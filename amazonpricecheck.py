# import dependencies
import requests
from bs4 import BeautifulSoup as bs
import smtplib
import time

# this function will send alert email


def sendmail(url):
    gmail_address = input("Enter your gmail address to send alert email: ")
    verification = input("Enter the 2-step verification code for gmail: ")
    dest_address = input(
        "Enter the email address you want to receive the alert email: ")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(gmail_address, verification)
    subject = "Price dropped!!!"
    body = "Check the price of the following item: \n" + url

    msg = (subject + "\n\n" + body)

    server.sendmail(
        gmail_address,
        dest_address,
        msg
    )

    print("Email has been sent")

# this function scrapes the website checks for the item's price


def pricecheck():
    url = input("Enter product's URL: ")

    wanted_price = input("What is your desired price? ")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}

    page = requests.get(url, headers=headers)

    soup = bs(page.content, 'html.parser')

    # print(soup.prettify)

    #title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:len(price)])

    wanted_price = float(input("What is your desired price? "))

    if converted_price <= wanted_price:
        sendmail(url)
    else:
        print("Item's price is", converted_price,
              "higher than your desired price", wanted_price)

    # print(title.strip())
    # print(converted_price)


# pricecheck()


# track the price every day
while True:
    pricecheck()
    time.sleep(3600*24)
