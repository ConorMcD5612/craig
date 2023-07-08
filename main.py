import time
import requests
import os
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup

load_dotenv()
email_pass = "icqzagqdzzltqdnb"
#min price = 900 max price = 1200, distance = around burlington 

CRAIG_URL = os.getenv('CRAIG_URL')

driver = webdriver.Chrome()

driver.get(CRAIG_URL)

time.sleep(5)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, "html.parser")

apartments = soup.find_all("div", class_ = "gallery-card")
#amount of posts that are in burlington area 
postings = int(soup.find("div", class_="count").get_text()[0])

apartment_info = []

#get info for each apartment 
for apartment in apartments[:postings]:
    print(apartment.find("span", class_="priceinfo").get_text())
    print(apartment.find("a", class_="main").get("href"))
    print(apartment.find("span", class_="label").get_text())
    apartment_info.append({
        "price": apartment.find("span", class_="priceinfo").get_text(),
        "title": apartment.find("a", class_="main").get("href"),
        "link": apartment.find("span", class_="label").get_text()
    }) 
     


print(apartment_info)

