import time

import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

SITE_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScjQcAqTJuUilUN5nlBnToSpfLDW4e2Pz35RZHn3e4O5HqDFg/viewform?usp=sf_link"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept-Language": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
response_text = requests.get(SITE_URL, headers=header).text
soup = BeautifulSoup(response_text, "html.parser")

# links, prices, addresses

li_list = soup.find_all("li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")
apartments_list = []


def add_new_record(app):
    link_tag = app.find(class_="StyledPropertyCardDataArea-anchor")
    app_link = link_tag["href"]
    app_address = link_tag.find("address").text.strip()
    app_address = app_address.replace(" | ", " ")
    app_price = app.find(class_="PropertyCardWrapper__StyledPriceLine").text
    app_price = app_price.replace(",", "").replace("+", "").replace("/mo", "").replace("1 bd", "").replace("1bd", "")
    app_price = app_price.strip()
    apartments_list.append({"link": app_link, "address": app_address, "price": app_price})


for aprtm in li_list:
    add_new_record(aprtm)

print(apartments_list)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_options)

for aprtm in apartments_list:
    driver.get(FORM_URL)
    time.sleep(1)
    inp = driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    inp.send_keys(aprtm["address"])
    inp = driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    inp.send_keys(aprtm["price"])
    inp = driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    inp.send_keys(aprtm["link"])
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()

driver.quit()
