# -*- coding: utf-8 -*-
## cookies
import pickle

## scraping and SQL
import json
import psycopg2
from bs4 import *

## configuration and sleep
import pyautogui
from configparser import ConfigParser
from time import sleep

## webdriver
from connectDB import connection
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

service = Service(verbose = True)

class App:
    def __init__(self, email= "", password= "",
                 path="", language="", main_url="", marketplace_url="", binary_location="", driver_location="", time_to_sleep=""):
        self.email = email
        self.password = password
        self.path = path
        self.language = language
        self.marketplace_options = None
        self.posts = None
        self.time_to_sleep = float(time_to_sleep)
        """with open('marketplace_options.json', encoding='utf-8') as f:
            self.marketplace_options = json.load(f)
            self.marketplace_options = self.marketplace_options[self.language]
        """
        # Options for driver
        options = Options()
        options.add_argument("dom-webnotifications-disabled")
        options.add_argument("-inprivate")
        ##self.driver_path = driver_location

        # INITIALIZE DRIVER (EDGE)
        self.driver = webdriver.Edge(options= options, executable_path= driver_location)
        self.driver.maximize_window()
        self.main_url = main_url
        self.marketplace_url = "https://www.facebook.com/marketplace/create/vehicle"
        self.driver.get(self.main_url)
        self.log_in()
        sleep(3)
        self.posts = self.fetch_all_posts()
        for post in self.posts:
            self.move_from_home_to_marketplace_create_item()
            sleep(3)
            self.create_post(post)

        self.driver.quit()


    def log_in(self):
        email_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(self.email)
        password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
        password_input.send_keys(self.password)
        login_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@type='submit']")))
        login_button.click()

    def move_from_home_to_marketplace_create_item(self):
        self.driver.get(self.marketplace_url)


    def add_photos_to_post(self, pics_path):
        pics_path = pics_path.lower()
        wait = WebDriverWait(self.driver, 10)

        picsXPATH='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[4]/div/div[1]/div/div/div[1]'
        photo_button = wait.until(EC.presence_of_element_located((By.XPATH, picsXPATH)))
        if not photo_button.is_displayed():
            raise Exception('Photo button is not visible')

        photo_button.click()
        sleep(2)
        pyautogui.hotkey('ctrl', 'l')
        sleep(self.time_to_sleep)
        pyautogui.write(self.path  + pics_path)
        sleep(self.time_to_sleep)
        pyautogui.press('enter')
        sleep(self.time_to_sleep)
        pyautogui.press('tab')
        sleep(self.time_to_sleep)
        pyautogui.press('tab')
        sleep(self.time_to_sleep)
        pyautogui.press('tab')
        sleep(self.time_to_sleep)
        pyautogui.press('tab')
        sleep(2)
        pyautogui.click(219, 251)
        pyautogui.hotkey('ctrl', 'a')
        sleep(self.time_to_sleep)
        pyautogui.press('enter')
        sleep(self.time_to_sleep)


    def add_text_to_post(self, brand, model, price, description):
        brandlink = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[8]/div/label/div/div/input"
        modellink = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[9]/div/label/div/div/input"
        pricelink = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[11]/div/div/label/div/div/input"
        desclink = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[18]/div/div/label/div/div/textarea"
        wait = WebDriverWait(self.driver, 20)
        ## scroll page
        sleep(1)
        pyautogui.moveTo(x=228, y=424) ## x = 228 and y = 424
        pyautogui.click()
        pyautogui.press("down", presses=3)
        ##
        brand_input = wait.until(EC.presence_of_element_located((By.XPATH, brandlink)))
        brand_input.send_keys(brand)

        model_input = wait.until(EC.presence_of_element_located((By.XPATH, modellink)))
        model_input.send_keys(model)

        price_input = wait.until(EC.presence_of_element_located((By.XPATH, pricelink)))
        price_input.send_keys(price)

        description_input = wait.until(EC.presence_of_element_located((By.XPATH, desclink)))
        description_input.send_keys(description)



    def ispublished(self, path):
        con = connection()
        try:
            cur = con.cursor()
            postgres_query = f"UPDATE camperdata SET ispublished = 1 WHERE path = '{path}';"
            cur.execute(postgres_query)
            cur.close()
        except psycopg2.Error as error:
            print("Something happened", error)
        finally:
            if(con):
                con.close()

    def fetch_all_posts(self):
        posts = None
        con = connection()
        try:
            cursor = con.cursor()
            postgres_query = f"SELECT * FROM camperdata WHERE ispublished = 0;"
            cursor.execute(postgres_query)
            posts = cursor.fetchall()
            cursor.close()

        except psycopg2.Error as error:
            print("Failed to read data from postgres table", error)

        finally:
            if (con):
                con.close()
        return posts


    def create_post(self, post):
        brand = post[5]
        model = post[6]
        price = post[4]
        desc = post[7]


        wait = WebDriverWait(self.driver, 20)
        pics_path = post[2]
        print(pics_path)
        self.add_photos_to_post(pics_path)

        category_link = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[3]/div/div/label'
        category_opt = '/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[4]'
        category_input = wait.until(EC.presence_of_element_located((By.XPATH, category_link)))
        category_input.click()

        category_option = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[4]/div[1]/div/div/span')))
        category_option.click()
        sleep(self.time_to_sleep)
        self.add_text_to_post(brand, model, price, desc)

        year_link="//*[@aria-label='Año']"

        year_input =  wait.until(EC.visibility_of_element_located((By.XPATH, year_link)))
        year_input.click()
        sleep(self.time_to_sleep)
        pyautogui.write(str(post[3])) ## 3 is the index position in the DB, that have the value of year.
        pyautogui.press('enter')
        sleep(self.time_to_sleep)


        extcolor = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Color del exterior']")))
        extcolor.click()
        sleep(self.time_to_sleep)

        pyautogui.write("b") ## write b to get color "blanco" option
        sleep(2)
        pyautogui.press("enter")
        sleep(self.time_to_sleep)

        intcolor =  wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Color del interior']")))
        intcolor.click()
        sleep(self.time_to_sleep)

        pyautogui.write("m") ## write m to get color "marron" option
        sleep(2)
        pyautogui.press("enter")
        sleep(self.time_to_sleep)

        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Siguiente']")))
        next_button.click()

##        self.post_in_more_places(post[9])
##        sleep(self.time_to_sleep)

        post_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Publicar']")))
        post_button.click()
        sleep(self.time_to_sleep)

        self.ispublished(post[2]) ## post[2] equal folder path of RV pics

    def get_element_position(self, key, specific):
        if specific in self.marketplace_options[key]:
            return str(self.marketplace_options[key][specific])
        return -1


    def post_in_more_places(self, groups):
        groups_positions = groups.split(",")

        for group_position in groups_positions:
            group_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='" + self.marketplace_options["labels"]["Marketplace"] +  "']/div/div/div/div[4]/div/div/div/div/div/div/div[2]/div[" + group_position + "]")))
            group_input.click()
            sleep(self.time_to_sleep)


if __name__ == '__main__':
    config_object = ConfigParser()
    config_object.read("config.ini")
    facebook = config_object["FACEBOOKUSER"]
    configuration = config_object["CONFIG"]
    app = App(facebook["email"], facebook["password"], configuration["images_path"], configuration["language"], facebook["main_url"], facebook["marketplace_url"], configuration["binary_location"], configuration["driver_location"], configuration["time_to_sleep"])