import requests
from bs4 import BeautifulSoup

craig_url = "https://vermont.craigslist.org/search/apa#search=1~gallery~0~0"

result = requests.get(craig_url).text

soup = BeautifulSoup(result, "html.parser")

apartments = soup.find(class_ = "cl-search-result")

print(apartments)


