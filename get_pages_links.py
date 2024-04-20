#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rosit
#
# Created:     13/07/2023
# Copyright:   (c) rosit 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from bs4 import *
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep

pages:list = []

def scrolling(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scroll(0, document.body.scrollHeight);")
        sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

def get_pages_links():

    options = Options()
    options.add_argument("dom-webnotificationes-disabled")
    options.add_argument("-inprivate")

    driver = webdriver.Edge(options = options, executable_path= r'C:\path\to\msedgedriver.exe')
    driver.maximize_window()
    driver.get('https://www.vhtrvs.com/shop')
    sleep(3)

    scrolling(driver)



    ## REAL BUSINESS
    html_content = driver.find_element(By.XPATH, '//*[@id="TPASection_kq1hr2yl"]/div/div/div/div/section')
    sleep(3)
    text = html_content.get_attribute("outerHTML")

    ##Beautiful soup part
    soup = BeautifulSoup(text, "html.parser")
    ##FIND ALL PRODUCTS in section of products

    products = soup.find_all("div",{"data-hook":"product-item-root"})
    length = len(products)

    for i in range(0,length):
        tag = products[i].find("a")
        page = tag["href"]
        pages.append(page)

    return pages
if __name__ == '__main__':
    get_pages_links()
