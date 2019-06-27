import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dealercode = 1

def extractdate(url, dealercode):
#website 1 
  page = urllib.request.urlopen(url)
  soup = BeautifulSoup(page)

  #store the car header
  title = str(soup.find_all(class_="title-content"))
  positionL = title.find("ListingDateBox_TitleText") #30 length
  fullheader = title[positionL+30:]
  positionR = fullheader.find("<")
  brandModelyear = fullheader[:positionR]
  extractyear = brandModelyear.find(" ")
  year = brandModelyear[:extractyear]
  brandModel = brandModelyear[extractyear+1:]


  #store all the car information for keydetail section
  title1 = str(soup.find_all(class_="motors-attribute-value"))
  allKeyDetails = title1.split("</span>")

  keyDetail1 = []
  for entry in allKeyDetails:
      lSymbol = entry.find(">")
      tempEntry = entry[lSymbol+1:]
      checkForSymbol = tempEntry.find("<")
      if (checkForSymbol != -1): #check whether can the symbol be found
        tempEntry = tempEntry[:checkForSymbol]
      if (tempEntry != ""): #check whether that particular label is empty or not
        keyDetail1.append(tempEntry)

  #store price of vehicle
  title2 = str(soup.find(class_="large-text buynow-details asking-price-text"))
  if (title2 == "None"):
    price = "Bidding - No Price"
  else: 
    extractPricePos1 = title2.rfind("</span>")
    extractFull = title2[:extractPricePos1]
    extractPricePos2 = extractFull.rfind(">")
    price = extractFull[extractPricePos2+1:]
  

  #consolidating details 
  model = keyDetail1[10]
  checkduplicate = brandModel.find(model)
  if (checkduplicate == "-1"):
    keyDetail1.append(brandModel)
  else:
    newModel = brandModel[:checkduplicate-1]
    keyDetail1.append(newModel)

  keyDetail1.append(year)
  keyDetail1.append(price)
  newkeyDetail = []
  for check in keyDetail1:
    if (check != "Yes" and check != "No"):
      newkeyDetail.append(check)

  requireInformation = [newkeyDetail[0], newkeyDetail[12],newkeyDetail[10], newkeyDetail[13], newkeyDetail[1], newkeyDetail[14], newkeyDetail[6], dealercode, newkeyDetail[5]]

  return requireInformation



def insertintoDB(singleData, dealercode):
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="shoesarcar"
  )

  mycursor = mydb.cursor()
  sql =  " INSERT INTO carinfo (carplatenumber, brand, model, yearofmanufactured, milleage, price, transmission,dealercode,enginecapacity) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
  insert_tuple = (singleData[0], singleData[1], singleData[2], singleData[3], singleData[4], singleData[5], singleData[6], singleData[7], singleData[8])
  mycursor.execute(sql, insert_tuple)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")
  dealercode += 1


urltest = "https://www.trademe.co.nz/motors/used-cars/holden/auction-2203458038.htm?rsqid=77406652aa6b40d58b6e1dae8d644e6e-001"


urltest1 = "https://www.trademe.co.nz/motors/used-cars/toyota/auction-2207225515.htm?rsqid=d1a45702bdb144e5b3a24f7efb34ef72-001"

urltest2 = "https://www.trademe.co.nz/motors/used-cars/mercedesbenz/auction-2207776231.htm?rsqid=7b28d9b8e8254592b7031e9ad1330357-001"
singleData = extractdate(urltest2, dealercode) 

insertintoDB(singleData, dealercode)

