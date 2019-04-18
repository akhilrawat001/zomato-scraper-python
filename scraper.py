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
import os,time,pprint,requests
from utils import *
from threading import Thread
DEBUG = True
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
************************************************
Task 1
************************************************
"""

def getLocalities():
    '''
    Returns a list of localities
    and the number of places 
    present in that location.
    ''' 
    if os.path.exists('data/localities.json') and DEBUG == True:
        data = readJsonFile('data/localities.json')
        return data
    else:
        soup = returnSoup(URL)
        div = soup.find("div", {"class" : "ui segment row"})
        aTags = div.findAll('a')
        localityDict = dict()
        for a in aTags:
            tempDict = dict()
            url = a.get('href')
            data = a.getText().strip().split('(')
            resturantName,places = data[0].strip(),data[-1].strip(')')
            tempDict['name'],tempDict['locations'],tempDict['url'] = resturantName,int(places.strip('places')),url
            localityDict[len(localityDict)+1] = tempDict.copy()
        writeJsonFile('data/localities.json',localityDict)
        return localityDict
# LOCALITYLIST = getLocalities()
# pprint.pprint(LOCALITYLIST)

"""
************************************************
Task 2
************************************************
"""
def scrapePage(url,num):
    print(url.split("?")[0].split(URL+"/")[1]+"_"+ str(num)+ ".json")
    print("Thread",num,"STARTED")
    tempList = []
    if os.path.exists("data/"+url.split("?")[0].split(URL+"/")[1]+"_"+ str(num)+ ".json"):
        data =readJsonFile("data/"+url.split("?")[0].split(URL+"/")[1]+"_"+ str(num)+ ".json")
        pprint.pprint(data)
    else:    
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
                pass 
                # contents[2] = float(contents[2])
                # contents[3] = int(contents[3].strip(" votes"))
            else:
                contents.insert(3,"NEW")
            contents.append(money)
            contents.append(iD)
            tempDict = dict()
            tempDict['resturantName'],tempDict['locality '],tempDict['rating'] = contents[0],contents[1],contents[2]
            tempDict['reviews'],tempDict['priceRange'],tempDict["resturnatID"] = contents[3],contents[4],contents[5]
            tempList.append(tempDict.copy())
    writeJsonFile("data/"+url.split("?")[0].split(URL+"/")[1]+"_"+ str(num)+ ".json",tempList)
    pprint.pprint(tempList)
    print("Thread",num,"ENDED")

def askUser():
    tempData = getLocalities()
    for key in tempData:
        print(key + ".",tempData[key]['name'])
    userInput = input('\nChoose any Locality : ')
    url = tempData[str(userInput)]['url'] + "?all=1&page=1"
    if os.path.exists('pageNumberCache/pageNumber.json') and DEBUG == True:
        data = readJsonFile('pageNumberCache/pageNumber.json')
        if url.split("?")[0] in data:
            NUMBER = data[url.split("?")[0]]
        else:
            soup = returnSoup(url)
            pNumber = soup.find("div", {"class" : "col-l-4 mtop pagination-number"})
            pNumber = int(pNumber.getText().split("of")[1].strip())
            data = readJsonFile('pageNumberCache/pageNumber.json')
            data[url.split("?")[0]] = pNumber
            writeJsonFile('pageNumberCache/pageNumber.json',data)
            NUMBER = pNumber
    else:
        soup = returnSoup(url)
        pNumber = soup.find("div", {"class" : "col-l-4 mtop pagination-number"})
        pNumber = int(pNumber.getText().split("of")[1].strip())
        data = dict()
        data[url.split("?")[0]] = pNumber
        writeJsonFile('pageNumberCache/pageNumber.json',data)
        NUMBER = pNumber
    for i in range(1,NUMBER+1):
        thread = Thread(target=scrapePage,args = (url[:-1]+ str(i),i,))
        thread.start()

askUser()