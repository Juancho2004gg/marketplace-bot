# -*- coding: utf-8 -*-
## scraping and SQL
import json
import psycopg2
from bs4 import *

## configuration and sleep
import pyautogui
from configparser import ConfigParser
from time import sleep

## webdriver
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

rvtopost = input("NAME OF RV TO POST?")
path = 'C:\/Users\/rosit\/OneDrive\/Documents\/proyecto python\/facebook-auto-post-main>'
class App:
    def __init__(self, email= "", password= "",
                 path="", language="", main_url="", marketplace_url="", binary_location="", driver_location="", time_to_sleep="", rvtopost=""):
        self.email = email
        self.password = password
        self.path = path
        self.language = language
        self.marketplace_options = None
        self.posts = None
        self.time_to_sleep = float(time_to_sleep)
        self.rvtopost = rvtopost
        """with open('marketplace_options.json', encoding='utf-8') as f:
            self.marketplace_options = json.load(f)
            self.marketplace_options = self.marketplace_options[self.language]
        """
        # Options for driver
        options = Options()
        options.binary_location = binary_location
        
        
        # INITIALIZE DRIVER (EDGE)
        self.driver = webdriver.Edge(service = Service(EdgeChromiumDriverManager.install(self)), options=options)
        self.driver.maximize_window()
        self.main_url = main_url
        self.marketplace_url = marketplace_url
        self.driver.get(self.main_url)
        self.log_in()
        self.move_from_home_to_marketplace_create_item()
        self.posts = self.fetch_all_posts(rvtopost)
        for post in self.posts:
            self.create_post(post)
        sleep(2)
        self.driver.quit()


    def log_in(self):
        email_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(self.email)
        password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
        password_input.send_keys(self.password)
        login_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@type='submit']")))
        login_button.click()


    def move_from_home_to_marketplace_create_item(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Marketplace"]')))
        self.driver.get(self.marketplace_url)


    def add_photos_to_post(self, post_folder):
        photolink='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[5]/div/div[2]/div/div'

        photo_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, photolink)))
        photo_button.click()
        sleep(2)
        pyautogui.hotkey('ctrl', 'l')
        sleep(self.time_to_sleep)
        pyautogui.write(self.path + post_folder)
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
        pyautogui.hotkey('ctrl', 'e')
        sleep(self.time_to_sleep)
        pyautogui.press('enter')
        sleep(self.time_to_sleep)


    def add_text_to_post(self, brand, model, price, description):
        brandlink='//*[@id="jsc_c_17"]'
        modellink='//*[@id="jsc_c_19"]'
        pricelink='//*[@id="jsc_c_1b"]'
        desclink='//*[@id="jsc_c_1d"]'


        brand_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, brandlink)))
        brand_input.send_keys(brand)

        model_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, modellink)))
        model_input.send_keys(model)

        price_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, pricelink)))
        price_input.send_keys(price)

        description_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, desclink)))
        description_input.send_keys(description)

##        brand_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='jsc_c_17']")))
##        brand_input.send_keys(brand)
##        pyautogui.write(brand)
##        sleep(2)


##        model_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Modelo']")))
##        model_input.click()
##        pyautogui.write(model)
##        sleep(2)
##
##        price_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Precio']")))
##        price_input.click()
##        pyautogui.write(str(price))

##        description_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Descripción']")))
##        description_input.send_keys(description)



    def ispublished(self, rvname):
        con = psycopg2.connect('articles.db')
        cur = con.cursor()
        postgres_query = """ UPDATE rv2 SET published = 1 WHERE path = '{rvname}'"""
        cur.execute(postgres_query)
        cur.close()
        
    def fetch_all_posts(self, rvtopost):
        posts = None
        try:
            conn = conn.connect('articles.db')
            cursor = conn.cursor()
            postgres_query = f"SELECT * FROM Campers WHERE ispublished = false"
            cursor.execute(postgres_query)
            posts = cursor.fetchall()
            cursor.close()

        except psycopg2.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            if (conn):
                conn.close()
        return posts


    def create_post(self, post):
        self.add_photos_to_post(post[6])

        category_link = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[3]/div/div/label'
        category_opt = '/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[4]'
        category_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, category_link)))
        category_input.click()

        category_option = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[4]/div[1]/div/div/span')))
        category_option.click()
        sleep(self.time_to_sleep)
        self.add_text_to_post(post[2], post[3], post[4], post[5])

        year_link="//*[@aria-label='Año']"

        year_input =  WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, year_link)))
        year_input.click()
        sleep(self.time_to_sleep)
        pyautogui.write(str(post[1]))
        pyautogui.press('enter')
        sleep(self.time_to_sleep)


        extcolor = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Color del exterior']")))
        extcolor.click()
        sleep(self.time_to_sleep)

        pyautogui.write("b")
        sleep(2)
        pyautogui.press("enter")
        sleep(self.time_to_sleep)

        intcolor =  WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Color del interior']")))
        intcolor.click()
        sleep(self.time_to_sleep)

        pyautogui.write("m")
        sleep(2)
        pyautogui.press("enter")
        sleep(self.time_to_sleep)

        next_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Siguiente']")))
        next_button.click()

##        self.post_in_more_places(post[9])
        sleep(self.time_to_sleep)

        post_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Publicar']")))
        post_button.click()
        sleep(self.time_to_sleep)

        self.ispublished(post[6])
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
    app = App(facebook["email"], facebook["password"], configuration["images_path"], configuration["language"], facebook["main_url"], facebook["marketplace_url"], configuration["binary_location"], configuration["driver_location"], configuration["time_to_sleep"], rvtopost)