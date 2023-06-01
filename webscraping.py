import psycopg2
from bs4 import *
import random
from connectDB import connection, insertValues
##from create_csv import writecsv
import json
import re
import requests
import os
# CREATE FOLDER
datos = dict()
URL = f"https://www.vhtrvs.com/product-page/"

def folder_create(img_links,folder_name):
    try:
        os.mkdir(folder_name)
    # if folder exists with that name, break
    except:
        print("Folder Exist with that name!")
        return 0

    # image downloading start
    download_images(img_links, folder_name)
def pageURL():
    # name of vehicle to post
    year_name = input("Ingresar año y nombre del vehiculo:")
    if year_name:
        year_name = year_name.lower()
        page = year_name.replace(" ","-")
        info = page.split("-")
        length = len(info) ## length of input 

    if length>3:
        datos["brand"] = info[1:3]
        datos["model"] = info[3::]

    else:
        datos["brand"] = info[1]
        datos["model"] = info[-1]

    datos["year"] = info[0]
    # take url
    return page


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

def database(info,page):
    try:
        con = connection()
        cur = con.cursor()
        ID = id(random.randint(1,100))
        
        ## scheme is (id, ispublished, path, price, year, make, model, description)
        values = (ID, 0, page, info['price'], info['year'],''.join(info['brand']), info['model'], info['desc'])
        insertValues(cur, values)
        
        con.commit()
    
    except psycopg2.Error as error:
        print(error)
    finally:
        if(con):
            con.close()
            

def editDescription(desc):
    d = (desc.lower()).encode('ascii', 'ignore').decode('ascii')

    return d
def scraping(page):
    VEHICLEPAGE = URL+page
    r = requests.get(VEHICLEPAGE)
    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')
    desc = soup.find('section', {'data-hook':'description-wrapper'}).get_text()
    datos["desc"] = editDescription(desc)
    
    price = soup.find('span', {'data-hook':'formatted-primary-price'}).get_text()
    regex = re.sub('[^\d\.]','',price).split('.')
    datos["price"] = int(regex[0])
    script= soup.find('script', {'id':'wix-warmup-data'})
    sc=script.text
    wix_warmup= json.loads(sc)

    return wix_warmup

##def createfile(page):
##    with open(f'{page}/{page}.txt', 'w') as f:
##        f.write(datos['year']+'\n')
##        f.write(str(datos['price'])+'\n')
##        f.write(datos['brand']+'\n')
##        f.write(datos['model']+'\n')
##        f.write(datos['desc'])

def main():
    valid = True
    while(valid):
        url = pageURL()
        wixdict = scraping(url)
        img_links=extract_img(wixdict, url)
        
        # Save info to database
        database(datos, url)
        
        # Call folder create function
        folder_create(img_links, url)
        likeToContinue = input("You want to continue? (1/0)")
        if likeToContinue == "0":
            valid = False
        else:
            valid = True




# CALL MAIN FUNCTION
main()