import requests
from bs4 import BeautifulSoup

URL = "https://www.amfiindia.com/downloads"

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')

for i in links:
    if 'Scheme Data Download' in i.text:
        url = i['href']
        response = requests.get(url)
        print("Ok")
    else:
        print('Site has been modified')