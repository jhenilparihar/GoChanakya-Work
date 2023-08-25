import requests
from bs4 import BeautifulSoup

URL = "https://www.amfiindia.com/downloads"

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')

flag = 0
for i in links:
    if 'Scheme Data Download' in i.text:
        url = i['href']
        requests.get(url)
        flag = 1
        break

if flag == 0:
    print("Error while scraping")
else:
    print("Scraped successfully!")