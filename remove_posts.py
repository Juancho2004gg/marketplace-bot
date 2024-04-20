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
import pickle ## cookies
from time import sleep
import pyautogui ## to scrolling

## inventory
from improvedScraping import super_scraping

## selenium and config

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from configparser import ConfigParser

copia = dict()
rvs_on_facebook = {'2018 coachmen catalina': '2018-coachmen-catalina', '2006 forest river surveyor': '2006-forest-river-surveyor', '2008 keystone vlite': '2008-keystone-vlite', '2022 dutchmen aspen trail': '2022-dutchmen-aspen-trail', '2006 crossroads zinger': '2006-crossroads-zinger', '2013 dutchmen dutchmen': '2013-dutchmen-dutchmen', '2022 open range': '2022-open-range', '2008 dutchmen dutchmen': '2008-dutchmen-dutchmen', '2018 keystone springdale': '2018-keystone-springdale', '2019 puma palomino': '2019-puma-palomino', '2015 forest river wildwood': '2015-forest-river-wildwood', '2014 forest river flagstaff': '2014-forest-river-flagstaff', '2015 cherokee patriot': '2015-cherokee-patriot', '2017 jayco jayflight 1': '2017-jayco-jayflight-1', '2021 kz sportsmen': '2021-kz-sportsmen', '2017 forest river wildwood': '2017-forest-river-wildwood', '2014 design royal travel': '2014-design-royal-travel', '2003 keystone hornet': '2003-keystone-hornet', '2009 keystone hornet': '2009-keystone-hornet', '2015 Forest River Wildwood': '2015-forest-river-wildwood', '2015 Forest River Cherokee': '2015-forest-river-cherokee', '2017 Jayco Jay flight': '2017-jayco-jay-flight', '2014 Design Travel': '2014-design-travel', '2020 K-Z Sportsmen': '2020-k-z-sportsmen', '2013 Coachmen Catalina Gris': '2013-coachmen-catalina-gris', '2011 Palomino Puma': '2011-palomino-puma', '2013 Dutchmen Beautiful': '2013-dutchmen-beautiful', '2022 OPEN RANGE': '2022-open-range', '2021 grand design': '2021-grand-design', '2000 Chevrolet Camaro': '2000-chevrolet-camaro', '2022 yamaha max': '2022-yamaha-max', '2022 suzuki king quad': '2022-suzuki-king-quad', '2016 Chevrolet Corvette': '2016-chevrolet-corvette', '2017 Lamborghini Huracan LP 580-2 Spyder Convertible 2D': '2017-lamborghini-huracan-lp-580-2-spyder-convertible-2d', '2003 Ford Mustang': '2003-ford-mustang', '2001 Ford F150 Regular Cab': '2001-ford-f150-regular-cab', '2016 starcraft ar one 34 ft bumper': '2016-starcraft-ar-one-34-ft-bumper', '2018 heartland prowler': '2018-heartland-prowler', '2014 cherokee 28ft 5th wheel': '2014-cherokee-28ft-5th-wheel', '2018 heartland north trail': '2018-heartland-north-trail', '2016 gulfstream conquest': '2016-gulfstream-conquest', '2017 coachmen cataina': '2017-coachmen-cataina', '2019 heartland pioneer': '2019-heartland-pioneer', '2013 puma palomino 32ft bumper': '2013-puma-palomino-32ft-bumper', '2014 cherokee cherokee': '2014-cherokee-cherokee', '2006 alumascape holiday rambler': '2006-alumascape-holiday-rambler', '2016 forest river wildwood': '2016-forest-river-wildwood', '2018 dutchmen coleman': '2018-dutchmen-coleman', '2016 spree escape': '2016-spree-escape', '2018 aspen trail': '2018-aspen-trail', '2015 starcraft slideout': '2015-starcraft-slideout', '2016 forest reiver wildwood 32ft': '2016-forest-reiver-wildwood-32ft', '2016 forest river salem 30ft': '2016-forest-river-salem-30ft', '2016 Wildwood 30 feet': '2016-wildwood-30-feet', '2017 greywolf 1 slide out 30ft': '2017-greywolf-1-slide-out-30ft', '2013 homette nomad 1 slide out 34ft': '2013-homette-nomad-1-slide-out-34ft', '2017 kz sportsman 33ft': '2017-kz-sportsman-33ft', '2011 forest river greywolf': '2011-forest-river-greywolf', '2012 viewfinder 27ft': '2012-viewfinder-27ft', '2006 keystone springdale': '2006-keystone-springdale', '2000 coachmen coachmen': '2000-coachmen-coachmen', '2016 forest river vibe extreme lite': '2016-forest-river-vibe-extreme-lite', '2015 keystone hideout': '2015-keystone-hideout', '2017 keystone bullet': '2017-keystone-bullet', '2015 forest river salem': '2015-forest-river-salem', '2019 heartland trailrunner': '2019-heartland-trailrunner', '2017 grand design imagine': '2017-grand-design-imagine', '2021 grand design solitude': '2021-grand-design-solitude', '2008 forest river wildwood': '2008-forest-river-wildwood', '2017 jayco jayflight': '2017-jayco-jayflight', '2021 cherokee artic wolf': '2021-cherokee-artic-wolf', '2018 starcraft ar one': '2018-starcraft-ar-one', '2019 dutchmen aspen trail': '2019-dutchmen-aspen-trail', '2006 keystone raptor': '2006-keystone-raptor', '2005 tahoe transport': '2005-tahoe-transport', '2016 jayco jayflight': '2016-jayco-jayflight', '2008 jayco jayflight': '2008-jayco-jayflight', '2022 kz sportsmen toy hauler': '2022-kz-sportsmen-toy-hauler', '2017 salem cruise lite': '2017-salem-cruise-lite', '2013 forest river cherokee': '2013-forest-river-cherokee', '2017 keystone hideout': '2017-keystone-hideout', '2018 forest river patriot': '2018-forest-river-patriot', '2014 coachmen freedom express': '2014-coachmen-freedom-express', '2019 forest river wildcat': '2019-forest-river-wildcat', '2018 forest river wildwood': '2018-forest-river-wildwood', '2009 forest river wildwood': '2009-forest-river-wildwood', '2013 cherokee shasta': '2013-cherokee-shasta', '2009 forest river windjammer': '2009-forest-river-windjammer', '2015 open range': '2015-open-range', '2016 forest river vibe': '2016-forest-river-vibe', '2010 keystone springdale': '2010-keystone-springdale', '2013 crossroads longhorn 33ft': '2013-crossroads-longhorn-33ft', '2013 forest river vcross platinum 41ft': '2013-forest-river-vcross-platinum-41ft', '2016 wildwood 30ft': '2016-wildwood-30ft', '2014 coachmenn catalina 2 slide out 37ft': '2014-coachmenn-catalina-2-slide-out-37ft', '2010 crossroads cruiser 3 slide out 35ft': '2010-crossroads-cruiser-3-slide-out-35ft', '2018 jayco jayflight': '2018-jayco-jayflight', '2007 jayco jayflight 1 slide out 32ft': '2007-jayco-jayflight-1-slide-out-32ft', '2015 heartland prowler 1 slide out 28ft': '2015-heartland-prowler-1-slide-out-28ft', '2014 redwood 39ft': '2014-redwood-39ft', '2015 avenger 36ft': '2015-avenger-36ft', '2019 forest river wildwood 35ft': '2019-forest-river-wildwood-35ft', '2015 gulfstream kingsport 30ft': '2015-gulfstream-kingsport-30ft', '2017 jayco jayflight 30ft': '2017-jayco-jayflight-30ft', '2015 springdale summerland 33ft': '2015-springdale-summerland-33ft', '2016 salem forest river': '2016-salem-forest-river', '2000 camaro z28': '2000-camaro-z28', '2022 yamaha rmax': '2022-yamaha-rmax', '2022 suzuki king quad 1': '2022-suzuki-king-quad-1', '2016 Chevrolet corvette': '2016-chevrolet-corvette', '2003 Ford harley davidson': '2003-ford-harley-davidson', '2014 salem forest river': '2014-salem-forest-river', '2016 forest river wildwood heritage glen': '2016-forest-river-wildwood-heritage-glen', '2008 keystone laredo 33ft 5th wheel': '2008-keystone-laredo-33ft-5th-wheel', '2003 skyline aljo 25ft bumper': '2003-skyline-aljo-25ft-bumper', '2007 four winds': '2007-four-winds', '2021 heartland prowler': '2021-heartland-prowler', '2019 keystone hideout': '2019-keystone-hideout', '2017 zinger z 1 lite': '2017-zinger-z-1-lite', '2007 forest river salem': '2007-forest-river-salem', '2014 skylark walkabout': '2014-skylark-walkabout', '2012 flagstaff vlite': '2012-flagstaff-vlite', '2010 crossroads zinger': '2010-crossroads-zinger', '2005 crossroad cruiser': '2005-crossroad-cruiser', '2005 pilgrim pilgrim': '2005-pilgrim-pilgrim', '2005 kz coleman': '2005-kz-coleman', '2012 puma palomino 35': '2012-puma-palomino-35', '2019 montana 42ft': '2019-montana-42ft', '2015 keystone springdale 35ft': '2015-keystone-springdale-35ft', '2012 riverside 2 slide out 35ft': '2012-riverside-2-slide-out-35ft', '2021 keystone sprinter 3 slide out 35ft': '2021-keystone-sprinter-3-slide-out-35ft', '2014 keystone hideout 35ft': '2014-keystone-hideout-35ft', '2011 forestriver salem 32ft': '2011-forestriver-salem-32ft', '2005 dutchmen dutchmen': '2005-dutchmen-dutchmen', '2005 jayflight 32ft': '2005-jayflight-32ft', '2015 jayco jayflight 32ft': '2015-jayco-jayflight-32ft', '2017 fgreywolforest river': '2017-fgreywolforest-river', '2017 Lamborghini Huracan': '2017-lamborghini-huracan', '2003 Ford mustang cobra svt convertible collectors edition': '2003-ford-mustang-cobra-svt-convertible-collectors-edition', '2013 holiday rambler heritage glen 34ft': '2013-holiday-rambler-heritage-glen-34ft', '2016 Gulfstream Conquest': '2016-gulfstream-conquest', '2018 JAYCO JAYFLIGHT': '2018-jayco-jayflight', '2003 Ford Harley Davidson': '2003-ford-harley-davidson', '2013 Jayco Jayflight': '2013-jayco-jayflight', '2014 Cherokee Limited': '2014-cherokee-limited', '2015 Keystone Hideout': '2015-keystone-hideout', '2007 Forest Salem': '2007-forest-salem', '2015 Primetime Lacrosse': '2015-primetime-lacrosse', '2018 Highland Open range': '2018-highland-open-range', '2006 Travel Trailer Rambler': '2006-travel-trailer-rambler', '2006 Sandpiper RV': '2006-sandpiper-rv', '2017 Heartland Big country': '2017-heartland-big-country', '2005 Pilgrim International RV': '2005-pilgrim-international-rv'}


class App:
    def __init__(self, email="",password="", login_url="",marketplace_url="",language="",binary_location="", driver_location=""):

        self.email = email;
        self.password = password;
        self.login_url = login_url;
        self.marketplace_url = marketplace_url;
        self.language = language; ## spanish
        self.binary_location = binary_location;
        self.driver_location = driver_location;

        self.rv_dict = rvs_on_facebook ## key is the name that each FB post have ## value is the path to compare in database

        self.inventory = list() ## rvs that are listed in the webpage vhtrvs.com

        ## options for microsoft edge
        options = Options()
        options.add_argument("dom-webnotificationes-disabled")
        options.add_argument("-inprivate")
        self.driver = webdriver.Edge(options = options,executable_path = driver_location)
        self.driver.maximize_window()

        ## load rvs that are in database
        self.check_inventory()

        sleep(2)

        ##login
        self.log_in()
        sleep(1)

        ## go to marketplace
        self.driver.get(self.marketplace_url)

        ## save the current inventory that fb marketplace account have.
        ##self.current_inventory()

        ## proceed to remove sold RVs
        self.remove_post()

    def check_inventory(self):
        self.inventory = super_scraping()

    def delete_button(self,wait):
        sleep(3)

        delete_xpath = "//*[@aria-label='Eliminar']"
        delete_button = wait.until(EC.presence_of_element_located((By.XPATH, delete_xpath)))
        delete_button.click()

    def confirm_button(self):
        sleep(2)
        xposition_button = 1186
        yposition_button = 640
        pyautogui.moveTo(xposition_button, yposition_button)
        sleep(2)
        pyautogui.click(xposition_button, yposition_button)
        pyautogui.click(xposition_button, yposition_button)
        pyautogui.click(xposition_button, yposition_button)
        sleep(4)

    def log_in(self):
        self.driver.get(self.login_url)
        cookies = pickle.load(open("cookies.pkl","rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def scrolling(self):
        SCROLL_PAUSE_TIME = 8
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scroll(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)

            new_height = self.driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

    def current_inventory(self): ## current inventory but listed on fb account
        return rvs_on_facebook
##        wait = WebDriverWait(self.driver, 20)
##        ##SCROLL PAGE
##
##        self.scrolling()
##
##        ## Get RV names
##        lists = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@aria-label, '20')]")))
##        for post in lists:
##            name = post.get_attribute("aria-label")
##
##            ## search_names
##            search = name
##
##            ## path to comparate in db
##            path = ("-".join(name.split(" "))).lower()
##
##            ## dictionary
##
##            self.rv_dict[search] = path
##        copia = self.rv_dict
##        print(copia)

    def remove_post(self):

        wait = WebDriverWait(self.driver, 20)
        search_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[2]/label/input"

        self.driver.execute_script("window.scroll(0, 0)")

        for search, path in self.rv_dict.items():
            print(search, path)
            if path not in self.inventory: ## if the posted RV is not in the inventory list, it means the RV has been sold.
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






if __name__ == '__main__':
    config = ConfigParser()
    config.read("config.ini")
    fb = config["FACEBOOKUSER"]
    files = config["CONFIG"]
    app = App(fb["email"],fb["password"],fb["main_url"], fb["marketplace_your_posts"], files["language"], files["binary_location"], files["driver_location"])
