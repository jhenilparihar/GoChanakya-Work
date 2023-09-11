from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from io import StringIO
import csv
import pandas as pd

def scheme_category(scheme):
    list_ = [i.replace("Scheme","").replace("&", "and").strip() for i in scheme.split(' - ')]
    if len(list_) < 2:
        return ["", list_[0]]
    return list_

def ISIN(x):
    isin_payout = ""
    isin_reinv = ""
    if '-' in x:
        x = x.split('-')
    else:
        x = x.split(' ')
    x = [i.strip() for i in x if len(i)>=12]
    if len(x)==1:
        x=x[0]
        if len(x)==24:
            isin_payout = x[0:12]
            isin_reinv = x[12:24]
        elif len(x)==12:
            isin_payout = x
    elif len(x)==2:
        if len(x[0]) == 12:
            isin_payout = x[0]
        if len(x[1]) == 12:
            isin_reinv = x[1]
    return [isin_payout, isin_reinv]

    return x

def amount(x):
    min_amount = ''
    x+=' '
    for i in range(len(x)):
        if x[i].isdigit():
            for k in x[i:]:
                if k.isdigit():
                    min_amount += k
                else:
                    return int(min_amount)
    return None


def download_csv():
    URL = "https://www.amfiindia.com/downloads"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    flag = 0
    csv_url =""
    for i in links:
        if 'Scheme Data Download' in i.text:
            csv_url = i['href']
            flag = 1
            break
    if flag == 0:
        print("Error while scraping")
    else:
        print("Scraped successfully!")
        response = requests.get(csv_url)
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(StringIO(content))
        
        with open('Schemes.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            for row in csv_reader:
                csv_writer.writerow(row)
        
def check_changes():
    new_df = pd.read_csv("./Schemes.csv")
    old_df = pd.read_csv("./Scheme-Master.csv")
    data = new_df[~new_df['Code'].isin(old_df['AMFICode'])]
    if len(data) > 0:
        bubbleData = pd.DataFrame({'AMC': data['AMC'], "AMFICode": data['Code'], 'SchemeName': data['Scheme Name'], 'SchemeType': data['Scheme Type'], 'AMFISchemeCategory': data['Scheme Category']})
        bubbleData[["SchemeCategory", "SubCategory"]] = bubbleData['AMFISchemeCategory'].apply(scheme_category).apply(pd.Series)
        bubbleData['SchemeNAVName'] = data['Scheme NAV Name']
        bubbleData['Fundtype'] = bubbleData['SubCategory'].apply(lambda x: 'FoF' if 'FoF' in x else 'DE')
        bubbleData['PlanType'] = bubbleData['SchemeNAVName'].apply(lambda x: 'Direct' if 'direct' in x.lower() else 'Regular')
        bubbleData[["ISINDivPayout_ISIN Growth", "ISINDivReinvestment"]] = data['ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment'].apply(str).apply(ISIN).apply(pd.Series)
        bubbleData['LaunchDate'] = data['Launch Date']
        bubbleData['ClosureDate'] = data[' Closure Date']
        bubbleData['AMFIMininmumAmount'] = data['Scheme Minimum Amount']
        bubbleData['SchemeMinimumAmount'] = data['Scheme Minimum Amount'].apply(str).apply(amount)
        bubbleData['isPrimary'] = bubbleData['SchemeNAVName'].apply(lambda x: 'Y' if 'growth' in x.lower() or 'regular' in x.lower() else 'N')
        new_df = pd.concat([old_df, bubbleData], ignore_index=True)
        # bubbleData.to_csv('Scheme-Master.csv', index=False)
        json = bubbleData.to_dict(orient='records')
        return json
    else:
        return []

app = Flask(__name__)

@app.route("/api", methods=["GET"])
def index():
    download_csv()
    data = check_changes()
    return jsonify(data)


if __name__ == "__main__":
    app.run()
