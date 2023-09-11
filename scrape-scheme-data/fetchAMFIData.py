import requests
from bs4 import BeautifulSoup
from io import StringIO
import csv
import pandas as pd

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
    