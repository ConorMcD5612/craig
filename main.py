import os
import ssl
import datetime
import smtplib
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import mailtrap as mt

load_dotenv()
EMAIL_PASS = os.getenv("EMAIL_PASS")
CRAIG_URL = os.getenv("CRAIG_URL")
EMAIL = os.getenv("EMAIL")
API = os.getenv("API")




# parse craigslist page into html
def get_apartments():
    #get html from craiglists page 
    page = requests.get(CRAIG_URL)
    soup = BeautifulSoup(page.content, "html5lib")
    
    #get apartments and that page 
    apartments = soup.find_all("li", class_="cl-static-search-result")
    print(apartments)
    
    return apartments

def get_info(apartments):
    apartment_info = [{
        "price": apartment.find("div", class_="price").get_text(),
        "link": apartment.find("a").get("href"),
        "title": apartment.find("div", class_="title").get_text()
    } for apartment in apartments]

    return apartment_info

def create_email(apartment_info):
    pass
    
    
    # get info for each apartment
    



html_content = ""
plain_content = ""
apartment_info = get_info(get_apartments())
# make strings
for apartment in apartment_info:
    html_content += f'<h1><a href="{apartment["link"]}">{apartment["title"]}</a></h1><h2>{apartment["price"]}</h2><br>'
    plain_content += (
        f'{apartment["title"]}  {apartment["price"]} \n {apartment["link"]}\n'
    )


plain_msg = MIMEText(plain_content, "plain")
html_msg = MIMEText(html_content, "html")


em = MIMEMultipart("alternative")
em["From"] = EMAIL
em["To"] = EMAIL
em["Subject"] = "New Apartment Listing"
em.attach(plain_msg)
em.attach(html_msg)


context = ssl.create_default_context()
message = f"""\
Subject: Hi Mailtrap
To: {EMAIL}
From: hello@demomailtrap.com

This is a test e-mail message."""

with smtplib.SMTP("live.smtp.mailtrap.io", 587) as server:
    server.starttls()
    server.login("api", API)
    server.sendmail("hello@demomailtrap.com", EMAIL, message)




# create mail object
