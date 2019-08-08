import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def mainpageextractionurl(main_url, dealercode): #extracting information from a single url
    page = urllib.request.urlopen(main_url)
    soup = BeautifulSoup(page,features="html.parser")
    allref = soup.find_all(class_="list-item premium-listing")

    keyData = {"Number plate": "", "Brand": "","Model detail": "","Year":"", "Kilometres": "", "Price": "", "Transmission": "", "Dealer Code": "", "Engine size": "" }

    for singleData in allref:
        singleData = str(singleData)
        pos1 = singleData.find("<img alt")
        pos2 = singleData.find("</ul>")
        requiredData = singleData[pos1:pos2]
        
        #Year/Brand/Model
        titlePos = requiredData.rfind("title")
        titleEndPos = requiredData.rfind("/>")
        titleRange = requiredData[titlePos+7:titleEndPos-1]
        yearBrandModel = titleRange.split(" ")

        keyData["Year"] = int(yearBrandModel[0])
        keyData["Brand"] = yearBrandModel[1]
        
        model = ""
        for i in range (2,len(yearBrandModel)):
            model += yearBrandModel[i]
        keyData["Model detail"] = model
      
        #Price 
        pricePos1 = requiredData.find("price")
        pricePos2 = requiredData.find("</p>")
        price = requiredData[pricePos1+7:pricePos2]
        keyData["Price"] = price

        #Rest of data
        mainInfoPos = requiredData.find("ul")
        extractData = requiredData[mainInfoPos:]
        extractDatav1 = extractData.split("</li")
        
        #milleage 
        milleagePos = extractDatav1[0].find("<li>")
        milleage = extractDatav1[0][milleagePos+4:]
        keyData["Kilometres"] = milleage
        
        #enginecap 
        enginecapPos1 = extractDatav1[2].find("<li>")
        enginecapPos2 = extractDatav1[2].rfind(" ")
        if (enginecapPos2 == -1):
            keyData["Engine size"] = extractDatav1[2][enginecapPos1+4:]
        else:
            enginecap = extractDatav1[2][enginecapPos1+4:enginecapPos2]
            keyData["Engine size"] = enginecap
            keyData["Transmission"] = extractDatav1[2][enginecapPos2:]

        #carplatenumber
        newCarPlate = getrandomcarplate()
        keyData["Number plate"] = newCarPlate
        currentNumber.append(keyData["Number plate"])

        dealercode += 1
        keyData["Dealer Code"] = int(dealercode) 

        insertintoDB(keyData)


def getrandomcarplate(): #generate random car platenumber
  tempCarplate = "temp"
  for n in range (1,5):
    tempCarplate +=  str(random.randint(1,9))
  while (tempCarplate in currentNumber):
    tempCarplate = "temp"
    for t in range (1,5):
      tempCarplate +=  str(random.randint(1,10))
  return tempCarplate

def getfinalpage(main_url): #locate the last page number
  page = urllib.request.urlopen(main_url)
  soup = BeautifulSoup(page,features="html.parser")
  allref = str(soup.find_all(class_="no-border"))
  pageInfoPos1 = allref.rfind("no-border")
  pageInfoPos2 = allref.rfind("</li>")
  updatedPageInfo = allref[pageInfoPos1+12:pageInfoPos2]
  findfirstspace = updatedPageInfo.find(" ")
  findsecondspace = updatedPageInfo.rfind(" ")
  pageNumber = updatedPageInfo[findfirstspace+1:findsecondspace]
  
  return pageNumber

def insertintoDB(singleData): #storing information into the database 
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="shoesarcar"
  )

  mycursor = mydb.cursor()
  sql =  " INSERT INTO autotradercarinfo (carplatenumber, brand, model, yearofmanufactured, milleage, price, transmission,dealercode,enginecapacity) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
  insert_tuple = []
  for data in singleData:
    insert_tuple.append(singleData[data])

  mycursor.execute(sql, insert_tuple)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")

#run main code
currentNumber = []
dealercode = 0
startingPage = "https://www.autotrader.co.nz/used-cars-for-sale?page=1"
mainpageextractionurl("https://www.autotrader.co.nz/used-cars-for-sale?page=1", dealercode)
finalPageNumber = int(getfinalpage("https://www.autotrader.co.nz/used-cars-for-sale?page=1"))
for i in range (2, finalPageNumber):
    dealercode += 20
    startingPageNumberPos = startingPage.find("=")
    updatedpageNumber = startingPage[:startingPageNumberPos] + str(i)
    mainpageextractionurl(updatedpageNumber,dealercode)
