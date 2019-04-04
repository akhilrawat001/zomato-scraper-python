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
import os,time,pprint
from utils import *

def returnSoup(url):
    '''
    This function returns data 
    parsed by BeautifulSoup
    '''
    driver = webdriver.Chrome()
    driver.get(url)
    response = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(response,'html.parser')
    driver.quit()
    return soup
URL = "https://www.zomato.com/ncr"

"""
***********************************************************************************************
Task 1
***********************************************************************************************
"""

def getLocalities():
    '''
    Returns a list of localities
    and the number of places 
    present in that location.
    ''' 
    if os.path.exists('data/localities.json'):
        data = readJsonFile('data/localities.json')
        return data
    else:
        soup = returnSoup(URL)
        div = soup.find("div", {"class" : "ui segment row"})
        aTags = div.findAll('a')
        localityList = list()
        for a in aTags:
            tempDict = dict()
            url = a.get('href')
            data = a.getText().strip().split('(')
            resturantName,places = data[0].strip(),data[-1].strip(')')
            tempDict['name'],tempDict['locations'],tempDict['url'] = resturantName,places,url
            localityList.append(tempDict.copy())
        writeJsonFile('data/localities.json',mainList)
        return localityList
# LOCALITYLIST = getLocalities()
# pprint.pprint(LOCALITYLIST)

"""
***********************************************************************************************
Task 2
***********************************************************************************************
"""
def scrapePage(url):
    soup = returnSoup(url)
    divs = soup.findAll("div",{ "class" : "content" })[1:-1]
    for div1 in divs:
        div = div1.find("div",{ "class" : "row" })
        allDiv = div.findAll('div')
        for i in allDiv:
            if i.get('data-res-id') != None:
                iD = int(i.get('data-res-id'))
        contents = [content for content in div.getText().strip().split('\n') if content != ""]
        contents = [ x.strip() for x in contents if x != '                                    ']
        if "SPONSORED" in contents:
            contents.pop(contents.index("SPONSORED"))
        contents.pop()
        if len(contents) == 5:
            contents.pop(0)
        money = [x.split(":₹")[1].strip() for x in div1.getText().strip().split('\n') if "Cost for two" in x]
        temp = ""
        for t in money[0]:
            if t not in ",":
                temp = temp + t
        money = int(temp)
        if "NEW" not in contents[2]: 
            contents[2] = float(contents[2])
            contents[3] = int(contents[3].strip(" votes"))
        else:
            contents.insert(3,"NEW")
        contents.append(money)
        contents.append(iD)
        tempDict = dict()
        tempDict['resturantName'],tempDict['locality '],tempDict['rating'] = contents[0],contents[1],contents[2]
        tempDict['reviews'],tempDict['priceRange'],tempDict["resturnatID"] = contents[3],contents[4],contents[5]
        print(tempDict)
scrapePage("https://www.zomato.com/ncr/rajouri-garden-delhi-restaurants?all=1&page=2")