import requests
import json
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(2)).strftime('%d-%b-%Y')
today = (datetime.now() - timedelta(1)).strftime('%d-%b-%Y')
URL = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={today}&todt={today}"
response = requests.get(f"{URL}")
data = response.text
data = data.split("\r\n")
data_filterd = [i for i in data if i]

keys = [
    "Scheme Code",
    "Scheme Name",
    "ISIN Div Payout/ISIN Growth",
    "ISIN Div Reinvestment",
    "Net Asset Value",
    "Repurchase Price",
    "Sale Price",
    "Date",
]
x = ""
y = ""

list_of_scheme = []
cnt=0
for i in data_filterd[1:]:
    cnt += 18
    if "Open Ended Schemes" in i:
        x = i
    elif ";" not in i:
        y = i
    else:
        scheme = {}
        for i, j in enumerate(i.split(";")):
            if i == 0 or i > 3:
                if i != 0 and i < 7:
                    if j != '':
                        scheme[keys[i]] = float(j)
                    else:
                        scheme[keys[i]] = None
                    continue
                scheme[keys[    i]] = j
        list_of_scheme.append(scheme)


file_path = "schemes.json"
file_ = open(file_path, "w")
json.dump(list_of_scheme, file_)
print(cnt)