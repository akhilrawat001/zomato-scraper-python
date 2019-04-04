"""
Scrap all localities and restaurants for a given link: 
https://www.zomato.com/ncr
Build two different kind of data from scraping
1. Localities
    Data to be scrapped:  
        1. Name of locality
        2. Total restaurants
2. Restaurant
    Data to be scrapped
        1. Name of restaurant
        2. Locality 
        3. Number of reviews
        4. Overall rating
        5. Restaurant Id
        6. Price range
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
#Task 1
#launch url
url = "https://www.zomato.com/ncr"
# create a new Chrome session
driver = webdriver.Firefox()
driver.get(url)
driver.quit()
response = driver.execute_script("return document.documentElement.outerHTML")
soup = BeautifulSoup(response.text,'html.parser')