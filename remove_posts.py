#-------------------------------------------------------------------------------
# Name:        remove posts
# Purpose:
#
# Author:      rosit
#
# Created:     21/07/2023
# Copyright:   (c) rosit 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pickle
from time import sleep
from connectDB import connection
import psycopg2
import pyautogui

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from configparser import ConfigParser

copia = dict()

class App:
    def __init__(self, email="",password="", login_url="",marketplace_url="",language="",binary_location="", driver_location=""):

        self.email = email;
        self.password = password;
        self.login_url = login_url;
        self.marketplace_url = marketplace_url;
        self.language = language; ## spanish
        self.binary_location = binary_location;
        self.driver_location = driver_location;

        self.rv_dict = dict() ## key is the name that each FB post have ## value is the path to compare in database

        self.dbdata = list() ## database data

        ## options for microsoft edge
        options = Options()
        options.add_argument("dom-webnotificationes-disabled")
        options.add_argument("-inprivate")
        self.driver = webdriver.Edge(options = options,executable_path = driver_location)
        self.driver.maximize_window()

        ## load rvs that are in database
        self.check_db()

        sleep(2)

        ##login
        self.log_in()
        sleep(1)

        ## go to marketplace
        self.driver.get(self.marketplace_url)

        ## save the current inventory that fb marketplace account have.
        self.current_inventory()

        ## proceed to remove sold RVs
        self.remove_post()
    def delete_button(self,wait):
        sleep(200)

        delete_xpath = "//*[@aria-label='Eliminar']"
        delete_button = wait.until(EC.presence_of_element_located((By.XPATH, delete_xpath)))
        delete_button.click()

    def confirm_button(self):
        sleep(2)
        xposition_button = 1186
        yposition_button = 640
        pyautogui.moveTo(xposition_button, yposition_button)

        pyautogui.click(xposition_button, yposition_button)

    def log_in(self):
        self.driver.get(self.login_url)
        cookies = pickle.load(open("cookies.pkl","rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()


    def current_inventory(self):
        wait = WebDriverWait(self.driver, 20)
        ##SCROLL PAGE

        SCROLL_PAUSE_TIME = 8
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scroll(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

        ##

        ## Get RV names
        lists = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@aria-label, '20')]")))
        for post in lists:
            name = post.get_attribute("aria-label")

            ## search_names
            search = name

            ## path to comparate in db
            path = ("-".join(name.split(" "))).lower()

            ## dictionary

            self.rv_dict[search] = path
        copia = self.rv_dict

    def remove_post(self):

        wait = WebDriverWait(self.driver, 20)
        search_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[2]/label/input"

        self.driver.execute_script("window.scroll(0, 0)")
        print(self.dbdata)

        for search, path in self.rv_dict.items():
            print(search, path)
            if path not in self.dbdata: ## if the posted RV is not in the database, it means the RV has been sold.
                print(path)
                sleep(3)
                search_bar = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
                search_bar.click()

                ## search posted RV with a name == search_name
                search_bar.send_keys(search)
                sleep(2)

                ## click post
                post_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[3]/div/div/span/div/div/div/div/div/div"
                post_button = wait.until(EC.presence_of_element_located((By.XPATH, post_xpath)))
                post_button.click()

                ## DELETE BUTTON
                self.delete_button(wait)

                ## confirmation
                self.confirm_button()

                sleep(3)
                self.driver.get(self.marketplace_url)

            else:
                continue



    def check_db(self):
        con = connection()
        try:
            cur = con.cursor()
            query = "SELECT path FROM camperdata;"
            cur.execute(query)

            ## save data to variable dbdata
            paths = cur.fetchall()
            for i in paths:
                path = ''.join(i)
                self.dbdata.append(path)
            cur.close()
        except(psycopg2.Error):
            print("something happened")
        finally:
            if(con):
                con.close()


if __name__ == '__main__':
    config = ConfigParser()
    config.read("config.ini")
    fb = config["FACEBOOKUSER"]
    files = config["CONFIG"]
    app = App(fb["email"],fb["password"],fb["main_url"], fb["marketplace_your_posts"], files["language"], files["binary_location"], files["driver_location"])
