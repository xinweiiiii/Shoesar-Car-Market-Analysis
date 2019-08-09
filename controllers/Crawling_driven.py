from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import random
import requests


def getMaxPageNumber(firstPageUrl): #Get the final page number
    req = Request(firstPageUrl, headers={'User-Agent': 'Mozilla/5.0'}) #change the web agent
    page = urlopen(req).read()
    soup = BeautifulSoup(page,features="html.parser")
    mainref = str(soup.find_all(class_="results-tags-wrapper"))
    selectedPage = mainref.split("</span>")
    selectedPage = selectedPage[1]
    maxPageNumberfront = selectedPage.find("of")
    maxPageNumber = selectedPage[maxPageNumberfront+3:]
    maxPageNumber = maxPageNumber.replace(",","")
    return int(maxPageNumber)

def getcarlisting(url): #retrieve all the vehicle data url and store into a list
    # maxPage = getMaxPageNumber(url)
    maxPage = 49
    pageSize = 0
    page = ""
    mainref = ""
    session = requests.Session()
    while pageSize < maxPage:
        req = session.post("https://www.driven.co.nz/used-cars-for-sale/", headers={'User-Agent': 'Mozilla/5.0'})
        # page = urlopen(req).read()
        page = BeautifulSoup(req.content)
        # soup = BeautifulSoup(page,features="html.parser")
        mainref = str(page.find_all(class_="listing-item"))

        pageSize += 24
        print(pageSize)

    print(mainref)



def mainpageextractionurl(main_url): #extracting information from a single url
    req = Request(main_url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page,features="html.parser")
    mainref = str(soup.find_all(class_="listing-table-info"))
    mainref = mainref.replace("\n","")
    print(mainref)

    keyData = {"Number plate": "", "Brand": "","Model detail": "","Year": "", "Kilometres": "", "Price": "", "Transmission": "", "Dealer Code": "", "Engine size": "" }

    listView = mainref.split("<tr>")
    # print(listView)
    listView = listView[1:]
    print(listView)

    for data in listView:
        if ("Make" in data):
            makePos1 = data.find("<td>Make</td>")
            makedetail = data[makePos1+17:]
            makePos2 = makedetail.find("</td>")
            makeData = makedetail[:makePos2]
            keyData["Brand"] = makeData

        if ("Model" in data):
            modelPos1 = data.find("<td>Model</td>")
            modelDetail = data[modelPos1+18:]
            modelPos2 = modelDetail.find("</td>")
            modelData = modelDetail[:modelPos2]
            keyData["Model detail"] = modelData

        if ("Year" in data):
            yearPos1 = data.find("<td>Year</td>")
            yearDetail = data[yearPos1+17:]
            yearPos2 = yearDetail.find("</td>")
            yearData = yearDetail[:yearPos2]
            keyData["Year"] = yearData

        if ("Odometer" in data):
            kiloPos1 = data.find("<td>Odometer</td>")
            kiloDetail = data[kiloPos1+21:]
            kiloPos2 = kiloDetail.find("</td>")
            kiloData = kiloDetail[:kiloPos2]
            keyData["Kilometres"] = kiloData

        if ("Transmission" in data):
            transPos1 = data.find("<td>Transmission</td>")
            transDetail = data[transPos1+25:]
            transPos2 = transDetail.find("</td>")
            transData = transDetail[:transPos2]
            keyData["Transmission"] = transData

        if ("Engine size" in data):
            engPos1 = data.find("<td>Engine size</td>")
            engDetail = data[engPos1+24:]
            engPos2 = engDetail.find("</td>")
            engData = engDetail[:engPos2]
            keyData["Engine size"] = engData

        newCarPlate = getrandomcarplate()
        keyData["Number plate"] = newCarPlate
        currentNumber.append(keyData["Number plate"])

        keyData["Dealer Code"] = int(dealercode)

    secondaryRef = str(soup.find_all(class_="listing-asking-price"))
    pricePos1 = secondaryRef.find("Now:")
    pricePos2 = secondaryRef.find("</strong>")
    priceDetail = secondaryRef[pricePos1+6:pricePos2]
    keyData["Price"] = priceDetail

    return keyData

def getrandomcarplate(): #Generate random car plate number
  tempCarplate = "temp"
  for n in range (1,5):
    tempCarplate +=  str(random.randint(1,9))
  while (tempCarplate in currentNumber):
    tempCarplate = "temp"
    for t in range (1,5):
      tempCarplate +=  str(random.randint(1,10))
  return tempCarplate

def insertintoDB(singleData): #Storing into the database
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost:8889",
    user="root",
    passwd="root",
    database="shoesarcar"
  )

  mycursor = mydb.cursor()
  sql =  " INSERT INTO turnercarinfo (carplatenumber, brand, model, yearofmanufactured, milleage, price, transmission,dealercode,enginecapacity) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
  insert_tuple = []
  for data in singleData:
    insert_tuple.append(singleData[data])

  mycursor.execute(sql, insert_tuple)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")

#Missing a try catch to show unsuccessful insertion and include the count
currentNumber = []
dealercode = 0
#mainpageextractionurl("https://www.driven.co.nz/used-cars-for-sale/nissan/leaf/auckland/onehunga/471687/")
getMaxPageNumber("https://www.driven.co.nz/used-cars-for-sale/")
getcarlisting("https://www.driven.co.nz/used-cars-for-sale/")
# #Run Main Code
# getTotalPage = getMaxPageNumber("https://www.turners.co.nz/Cars/Used-Cars-for-Sale/?sortorder=7&pagesize=24&pageno=1")
# dealercode = 0
# currentNumber = []
# for i in range (1,getTotalPage):
#     tempUrl = "https://www.turners.co.nz/Cars/Used-Cars-for-Sale/?sortorder=7&pagesize=24&pageno=" + str(i)
#     pageUrl = getcarlisting(tempUrl)
#     for one in pageUrl:
#         updateUrl = "https://www.turners.co.nz" + one
#         dealercode += 1
#         dataDict = mainpageextractionurl(updateUrl, dealercode)
#         insertintoDB(dataDict)
