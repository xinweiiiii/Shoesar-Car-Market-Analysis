import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


def extractdata(url, dealercode): #extracting information from a single url

    keyData = {"Number plate": "", "Brand": "","Model detail": "","Year":"", "Kilometres": "", "Price": "", "Dereg Value": "", "Transmission": "", "Dealer Code": "", "Engine size": ""}
    #website 1 

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,features="html.parser")
    title = str(soup.find_all(class_="box font_12"))
    title1 = str(soup.find_all(class_="gray_banner_text"))
    listTitle = title.split("</tr>")

    #make
    poshref = title1.find("href")
    tempPos = title1[poshref:]
    poshref1 = tempPos.find(">")
    tempPos1 = tempPos[poshref1:]
    poshref2 = tempPos1.find("</a")
    makeModel = tempPos1[1:poshref2]
    
    #model
    makepos1 = makeModel.find(" ")
    keyData["Brand"] = makeModel[:makepos1]
    keyData["Model detail"] = makeModel[makepos1+1:]


    #price
    priceData = listTitle[0]
    posPrice1 = priceData.find("$")
    priceDataTemp = priceData[posPrice1:]
    posPrice2 = priceDataTemp.find("</")
    finalPrice = priceDataTemp[:posPrice2]
    keyData["Price"] = finalPrice
    
    #date 
    dateData = listTitle[1]
    posDate1 = dateData.rfind("<br/>")
    tempDate = dateData[:posDate1]
    posDate2 = tempDate.rfind("-")
    finalDate = tempDate[posDate2+1:posDate1]
    keyData["Year"] = finalDate

    #milleage 
    milleageData = listTitle[2]
    posMilleage1 = milleageData.find("row_info")
    tempMilleage = milleageData[posMilleage1:]
    posMilleage2 = tempMilleage.find("(")
    finalMilleage = tempMilleage[10:posMilleage2].strip("\r\n").strip(" ")
    keyData["Kilometres"] = finalMilleage
    
    alldata = listTitle[2].split("row_title")

    #dereg value
    deregData = alldata[3]
    posDereg1 = deregData.find("$")
    deregTemp = deregData[posDereg1:]
    posDereg2 = deregTemp.find(" ")
    finalderegvalue = deregTemp[:posDereg2]
    keyData["Dereg Value"] = finalderegvalue

    #engine
    engine = alldata[5]
    posengine1 = engine.find("row_info")
    posengine2 = engine.find("cc")
    finalengine = engine[posengine1+10:posengine2].strip("\r\n\t\t\t\t\t\t\t\t\t").strip(" ")
    keyData["Engine size"] = finalengine

    #transmission
    trans = alldata[8]
    postrans1 = trans.find("row_info")
    temptrans = trans[postrans1:]
    postrans2 = temptrans.find("</div>")
    finaltrans = temptrans[10:postrans2]
    keyData["Transmission"] = finaltrans


    #carplatenumber
    newCarPlate = getrandomcarplate()
    keyData["Number plate"] = newCarPlate
    currentNumber.append(keyData["Number plate"])

    dealercode += 1
    keyData["Dealer Code"] = int(dealercode) 

    return keyData

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
    allref = str(soup.find_all(class_="font_bold font_12"))
    poslastdata = allref.rfind("</a>")
    allref1 = allref[:poslastdata]
    poslastdata1 = allref1.find(">")
    lastpage1 = allref1[-poslastdata1:]
    lastpagepos = lastpage1.find(">")
    lastpage = lastpage1[lastpagepos+1:]

    return lastpage


def getindvidual(main_url): #locate the last page number
    page = urllib.request.urlopen(main_url)
    soup = BeautifulSoup(page,features="html.parser")
    allref = str(soup.find_all('a', href=True))
    listofInfo = allref.split("<a")
    checkarray = []
    for i in listofInfo:
        if "info.php" in i:
            checkarray.append(i)
    
    newarray = []
    for j in checkarray:
        findhrefpos = j.find("href")
        findhrefpos1 = j.find(">")
        result = j[findhrefpos+6:findhrefpos1-1]
        newarray.append(result)

    return newarray

def insertintoDB(singleData): #storing information into the database 
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="shoesarcar"
  )

  mycursor = mydb.cursor()
  sql =  " INSERT INTO sgcarmart (carplatenumber, brand, model, yearofmanufactured, milleage, price, deregvalue, transmission,dealercode,enginecapacity) VALUES (%s, %s, %s,%s,%s,%s,%s, %s,%s,%s)"
  insert_tuple = []
  for data in singleData:
    insert_tuple.append(singleData[data])

  mycursor.execute(sql, insert_tuple)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")


    

#run main code
currentNumber = []
dealercode = 0
final = getfinalpage("https://www.sgcarmart.com/used_cars/listing.php?BRSR=0&RPG=20")
startingPage = "https://www.sgcarmart.com/used_cars/listing.php?BRSR=0&RPG=20"
allpageData = set(getindvidual(startingPage))
for single in allpageData:
    urlsingle = "https://www.sgcarmart.com/used_cars/" + single
    data = extractdata(urlsingle, dealercode)
    insertintoDB(data)
tempvalue = 0
for i in range(2, final):
    tempvalue += 20
    startingpage1 = "https://www.sgcarmart.com/used_cars/listing.php?BRSR=" + tempvalue + "&RPG=20"
    allpageData = set(getindvidual(startingPage))
    for single in allpageData:
        urlsingle = "https://www.sgcarmart.com/used_cars/" + single
        data = extractdata(urlsingle, dealercode)
        insertintoDB(data)
    
