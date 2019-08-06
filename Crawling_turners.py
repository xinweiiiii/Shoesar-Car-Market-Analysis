from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


def getMaxPageNumber(firstPageUrl):
    req = Request(firstPageUrl, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page,features="html.parser")
    mainref = str(soup.find_all(class_="results-pagelink"))
    selectedPage = mainref.split(",")
    listOfNum = []
    for singleData in selectedPage:
        if ("data-pageno" in singleData):
            pagePos1 = singleData.find("href")
            pagePos2 = singleData.rfind("</a>")
            addPage = singleData[pagePos1+9:pagePos2]
            if (addPage.isdigit()):
                listOfNum.append(int(addPage))
    return max(listOfNum)

def getcarlisting(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page,features="html.parser")
    mainref = str(soup.find_all(class_="green"))
    listUrl = mainref.split(",")
    singlePageUrl = []
    for singleurl in listUrl:
        findhrefpos = singleurl.find("href")
        findhrefendpos = singleurl.rfind(">View")
        cleanUrl = singleurl[findhrefpos+6:findhrefendpos-1]
        singlePageUrl.append(cleanUrl)
    
    return singlePageUrl

def mainpageextractionurl(main_url, dealercode):
    req = Request(main_url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page,features="html.parser")
    mainref = str(soup.find_all(class_="buy-now-header desktop"))
    
    keyData = {"Number plate": "", "Brand": "","Model detail": "","Year":"", "Kilometres": "", "Price": "", "Transmission": "", "Dealer Code": "", "Engine size": "" }

    #price
    pricePos1 = mainref.find("<p>")
    pricePos2 = mainref.find("</p>")
    extractPart1Info = mainref[pricePos1+3:pricePos2]
    dollarPos = extractPart1Info.find("$")
    extractFinalPrice = extractPart1Info[dollarPos:]
    keyData["Price"] = extractFinalPrice

    secondaryRef = str(soup.find_all(class_="table-module"))
    listView = secondaryRef.split("row-detail")
    newView = listView[1:]
    #print(newView)
    for data in newView:
        #vehicle 
        if ("Vehicle" in data):
            pricePos1 = data.find("row-value")
            vehicleDetail = data[pricePos1+11:]
            pricePos2 = vehicleDetail.find("</div")
            vehicleData = vehicleDetail[:pricePos2]
            brandmodel = vehicleData.split(" ")
            keyData["Brand"] = brandmodel[0]
            keyData["Model detail"] = brandmodel[1]
        
        #year
        if ("Year" in data):
            yearPos1 = data.find("row-value")
            yearDetail = data[yearPos1+11:]
            yearPos2 = yearDetail.find("</div")
            yearData = yearDetail[:yearPos2]
            keyData["Year"] = yearData
        
        #Transmission
        if ("Transmission" in data):
            transPos1 = data.find("row-value")
            transDetail = data[transPos1+11:]
            transPos2 = yearDetail.find("</div")
            transData = transDetail[:transPos2]
            keyData["Transmission"] = transData

        #Odometer
        if ("Odometer" in data):
            odoPos1 = data.find("row-value")
            odoDetail = data[odoPos1+15:]
            odoPos2 = odoDetail.find("\r\n")
            odoData = odoDetail[:odoPos2]
            keyData["Kilometres"] = odoData.lstrip(" ")
            
        #Engine
        if ("Engine" in data):
            engPos1 = data.find("row-value")
            engDetail = data[engPos1+11:]
            engPos2 = engDetail.find("</div")
            engData = engDetail[:engPos2]
            keyData["Engine size"] = engData
          
    
    newCarPlate = getrandomcarplate()
    keyData["Number plate"] = newCarPlate
    currentNumber.append(keyData["Number plate"])

    keyData["Dealer Code"] = dealercode

    return keyData

def getrandomcarplate():
  tempCarplate = "temp"
  for n in range (1,5):
    tempCarplate +=  str(random.randint(1,9))
  while (tempCarplate in currentNumber):
    tempCarplate = "temp"
    for t in range (1,5):
      tempCarplate +=  str(random.randint(1,10))
  return tempCarplate
        
def insertintoDB(singleData):
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="shoesarcar"
  )

  mycursor = mydb.cursor()
  sql =  " INSERT INTO carinfo4 (carplatenumber, brand, model, yearofmanufactured, milleage, price, transmission,dealercode,enginecapacity) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
  insert_tuple = []
  for data in singleData:
    insert_tuple.append(singleData[data])

  mycursor.execute(sql, insert_tuple)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")

 
        


getTotalPage = getMaxPageNumber("https://www.turners.co.nz/Cars/Used-Cars-for-Sale/?sortorder=7&pagesize=24&pageno=1")

dealercode = 0
currentNumber = [] 
for i in range (1,getTotalPage):
    tempUrl = "https://www.turners.co.nz/Cars/Used-Cars-for-Sale/?sortorder=7&pagesize=24&pageno=" + str(i)
    pageUrl = getcarlisting(tempUrl)
    for one in pageUrl:
        updateUrl = "https://www.turners.co.nz" + one
        dealercode += 1
        dataDict = mainpageextractionurl(updateUrl, dealercode)
        insertintoDB(dataDict)


        
