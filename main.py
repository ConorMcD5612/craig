import time
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

load_dotenv()
EMAIL_PASS = os.getenv("EMAIL_PASS")
CRAIG_URL = os.getenv("CRAIG_URL")
EMAIL = os.getenv("EMAIL")

hour = datetime.datetime.now().hour

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

#stops at 9pm
while(hour != 21):
   
    

    driver.get(CRAIG_URL)
    time.sleep(5)

    content = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(content, "html.parser")

    apartments = soup.find_all("div", class_="gallery-card")

    # amount of posts that are in area (search params)
    postings = int(soup.find("div", class_="count").get_text()[0])

    apartment_info = []
    # get info for each apartment
    for apartment in apartments[:postings]:
        uptime = apartment.find("div", class_="meta").get_text()

        # if not made in the last hour exit program
        if "min" in uptime:
            apartment_info.append(
                {
                    "price": apartment.find("span", class_="priceinfo").get_text(),
                    "link": apartment.find("a", class_="main").get("href"),
                    "title": apartment.find("span", class_="label").get_text(),
                }
            )


    if len(apartment_info) == 0:
        time.sleep(3600)#sleep 1hr
        driver.close() 
        continue 


    html_content = ""
    plain_content = ""

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
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login("conordmcdevitt@gmail.com", EMAIL_PASS)
        smtp.sendmail(EMAIL, EMAIL, em.as_string())

    driver.close()
    hour = datetime.datetime.now().hour
    time.sleep(3600)
