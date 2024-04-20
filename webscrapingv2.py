import shutil ##library to delete a folder with files


import psycopg2
from bs4 import *
import PySimpleGUI as sg
import random
from connectDB import connection, insertValues, createTable
##from create_csv import writecsv
import json
import re
import requests
import os
from improvedScraping import super_scraping
# CREATE FOLDER
datos = dict()
## scheme is (id, ispublished, path, year, price, make, model, description)

def folder_create(img_links,folder_name):
    try:
        os.mkdir(folder_name)
    # if folder exists with that name, break
    except:
        print("Folder Exist with that name!")
        return 0
    # image downloading start
    download_images(img_links, folder_name)

def extractName(page):
    # name of vehicle to post
    info = page.split("-")
    length = len(info)


    if length > 3: ## three because a normal name is year-brand-model, this has a length of three when we splited it

        datos["brand"] = info[1] ## POSITION 1 = BRAND NAME
        datos["model"] = " ".join(info[2::]) ##POSSIBLY POSITION 2 = MODEL NAME

    else:
        datos["brand"] = info[1]
        datos["model"] = info[-1]

    # take url
    return page


def extractYear(page):
    print(page)
    year_name = page.lower()
    page = year_name.replace(" ","-")
    info = page.split("-")
    datos["year"] = info[0]

def download_images(img_links,folder_name):

    # initial count is zero
    count = 0

    for i, link in enumerate(img_links):
        try:
            r = requests.get(link).content
            try:

                # possibility of decode
                r = str(r, 'utf-8')

            except UnicodeDecodeError:

                # After checking above condition, Image Download start
                with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                    f.write(r)

                # counting number of image downloaded
                count += 1
        except:
            pass



    print(f"Total {count} Images Downloaded")

def extract_img(wixdict,page):
    links = []
    warmup = wixdict['appsWarmupData']
    productid= list(warmup)[0]
    formato = f'productPage_USD_{page}'
    productpage= wixdict['appsWarmupData'][productid][formato]['catalog']['product']['media']

    for data in productpage:
        for key, value in data.items():
            if key=='fullUrl':
                links.append(value)
    return links

def database(datos,page):
    try:
        con = connection()
        cur = con.cursor()
        ID = id(random.randint(1,1000000))

        ## scheme is (id, ispublished, path, year, price, make, model, description)
        values = (ID, 0, page, datos['year'], datos['price'], datos['brand'], datos['model'], datos['desc'])
        insertValues(cur, values)

        con.commit()

    except psycopg2.Error as error:
        print(error)
    finally:
        if(con):
            con.close()


def extractDesc(desc):
    d = (desc.lower()).encode('ascii', 'ignore').decode('ascii')

    datos["desc"] = d

def scraping(page):
    r = requests.get(page)

    soup = BeautifulSoup(r.text, 'html.parser')

    desc = soup.find('section', {'data-hook':'description-wrapper'}).get_text()


    price = soup.find('span', {'data-hook':'formatted-primary-price'}).get_text()
    regex = re.sub('[^\d\.]','',price).split('.')

    ## values of database
    extractDesc(desc) # description
    datos["price"] = int(regex[0])
    ##
    script = soup.find('script', {'id':'wix-warmup-data'})
    sc = script.text
    wix_warmup = json.loads(sc)

    return wix_warmup


def remove_duplicates():
    query = """DELETE FROM camperdata WHERE id not in (SELECT min(id) FROM camperdata GROUP BY path); """
    try:
        con = connection()
        cur = con.cursor()

        cur.execute(query) ## delete duplicates
        cur.close()
        con.commit()

    except psycopg2.Error as error:
        print(error)

    finally:
        if(con):
            con.close()
def main():
    """
    This part is Creating a table
    """
    con = connection()
    cur = con.cursor()
    createTable(cur)

    cur.close()
    con.commit()
    con.close()

    ## ELIMINATE OLD RVS PICTURES

    try:
        shutil.rmtree('RVs')
    except:
        pass
    finally:
        os.mkdir('RVs')

    pagelinks = super_scraping() ## importing super_scraping function
    for link in pagelinks:
        page = re.sub(".*product-page/", "", link)
        folder_name = 'RVs\/' + page

        ## find preload imgs
        wixdict = scraping(link)

        extractName(page) ## extract brand and model for DB
        extractYear(page) ## extract year for DB

        img_links = extract_img(wixdict, page)

        # Call folder create function
        folder_create(img_links, folder_name) # the folder function has a download img function

        # Save info to database
        database(datos, page)

    remove_duplicates()


main()
if __name__ == "main":
    pass