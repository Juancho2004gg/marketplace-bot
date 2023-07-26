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
from time import sleep

pages:list = []

def super_scraping():

    driver = webdriver.Edge(executable_path=r'C:\path\to\msedgedriver.exe')
    driver.get('https://www.vhtrvs.com/shop')
    sleep(3)
    ## FIRST BUTTON
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/main/div/div/div/div[2]/div/div/div/section/div[2]/div/div/div/div/div/div/section/div/button')
    button.click()
    sleep(3)

    ## SECOND BUTTON

    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/main/div/div/div/div[2]/div/div/div/section/div[2]/div/div/div/div/div/div/section/div/button')
    button.click()
    sleep(3)

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
    super_scraping()