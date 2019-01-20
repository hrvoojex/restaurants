#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import pandas as pd 
import requests
import random
import time
import re


nameList = []
addressList = []
phoneList = []
df = pd.DataFrame()


searchUrl = ['https://www.yelp.co.uk/']
searchWord = ['Restaurants']
searchCity = ['Leeds', 'Birmingham', ' Glasgow']

page = 1
restaurantNum = 0
firstPage = True
condition = True

for city in searchCity:
    nameList = []
    condition = True

    while condition:
        headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

        #https://www.yelp.co.uk/search?find_desc=Restaurants&find_loc=London&start=0
        site_url = (searchUrl[0] + 'search?find_desc=' + searchWord[0] + 
                '&find_loc=' + city + '&start=' + str(restaurantNum))

        try:
            # Request web restaurantNum with GET
            response = requests.get(site_url, headers=headers)
            print(response)  # 200 for OK
            htmlSoup = BeautifulSoup(response.text, 'lxml')

            # Find a number of pages for searched word only on first restaurantNum
            if restaurantNum == 0:
                numPages = htmlSoup.find_all('span', class_='lemon--span__373c0__1xR0D text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_')[0].text
                numPages = numPages.split(' ')
                numPages = numPages[-1]  # 435

            aTagContainer = htmlSoup.find_all('a', class_='lemon--a__373c0__1_OnJ link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5')

            # Name
            if aTagContainer != []:
                for aTag in aTagContainer[::2]:
                    if aTag.contents[0] != 'read more' and aTag.contents[0] != 'More Topics':
                        nameList.append(aTag.contents[0])

            time.sleep(random.randint(1,2))
            restaurantNum += 30
        except:
            print(response)
        finally:
            page += 1
            if page > int(numPages):
                condition = False

                record = pd.Series(nameList)  # Convert list to pandas Series obj
                df[city] = record  # Write Series obj to a new column
                print(df)
            

writer = pd.ExcelWriter('yelp_restaurants.xlsx', engine='openpyxl')
df.to_excel(writer, sheet_name='Restaurants', index=False)  # Don't add index number at the beginning
writer.save()
print('')
