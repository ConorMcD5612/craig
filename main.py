import os
import smtplib
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium_stealth import stealth 
import mailtrap as mt
import time
import requests
import json

load_dotenv()
EMAIL_PASS = os.getenv("EMAIL_PASS")
CRAIG_URL = os.getenv("CRAIG_URL")
EMAIL = os.getenv("EMAIL")
API = os.getenv("API")
SENDER = os.getenv("SENDER")

#think have to give up on dynamic not good enough at web scraping to know how to do this 
#can have so it scrapes every 24 hours and sends email with new listings
def main():
    #start selenium browser and get html from craiglists page

    
    res = requests.get(CRAIG_URL)
    
    apartments = get_apartments(res.content)
    print(apartments)
    
    apartment_info = get_info(apartments)
    #em = create_email(apartment_info)
    #send_email(em)
    
    

# parse craigslist page into html
def get_apartments(html):

    #parse html
    
    soup = BeautifulSoup(html, "html.parser")
   
    apartments = soup.find_all("li", class_="cl-static-search-result")
    
    
    return apartments[:10]

def get_info(apartments):
    apartment_info = [{
        "price": apartment.find("div", class_="price").get_text(),
        "link": apartment.find("a").get("href"),
        "title": apartment.find("div", class_="title").get_text(),
    } for apartment in apartments]

    return apartment_info

def create_email(apartment_info):
    html_content = ""
    plain_content = ""
    plain_msg = MIMEText(plain_content, "plain")
    html_msg = MIMEText(html_content, "html")


    em = MIMEMultipart("alternative")
    em["From"] = SENDER
    em["To"] = EMAIL
    em["Subject"] = "New Apartment Listing"
    em.attach(plain_msg)
    em.attach(html_msg)

    for apartment in apartment_info:
        html_content += f'<h1><a href="{apartment["link"]}">{apartment["title"]}</a></h1><h2>{apartment["price"]}</h2><br>'
        plain_content += (
            f'{apartment["title"]}  {apartment["price"]} \n {apartment["link"]}\n'
        )
    return em

#don't want everything returning should just be past 24 hrs 
def send_email(em):

    with smtplib.SMTP("live.smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login("api", API)
        server.sendmail("hello@demomailtrap.com", EMAIL, em.as_string())
        
    # get info for each apartment

# will have it so it filters out listing that have already been emailed
    # json dump send lists
    #empty out once a week or something 
    # send ones that aren't in json
def check_if_sent(apartment_info) -> list:
    seen_apartments = []
    if os.path.exists("apartments_seen.json"):
        with open("apartments_seen.json", "r") as f:
            seen_apartments = json.load(f)
    

    #return unseen apartments 



main()






