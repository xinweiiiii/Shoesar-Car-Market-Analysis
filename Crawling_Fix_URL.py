import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dealercode = 1

def extractdate(url, dealercode):

  keyData = {"Number plate": "", "Brand": "","Model detail": "","Year":"", "Kilometres": "", "Price": "", "Transmission": "", "Dealer Code": "", "Engine size": "" }
#website 1 
  page = urllib.request.urlopen(url)
  soup = BeautifulSoup(page,features="html.parser")

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
  title1 = str(soup.find_all(class_="attributes-box key-details-box"))
  allKeyDetails = title1.split("</li>")
  
  keyAttribute = ["Number plate", "Kilometres", "Engine size", "Transmission", "Model detail"]
  
  for attribute in keyAttribute:
    for entry in allKeyDetails:
      if (attribute in entry):
        extractattribute = entry.split("</span>")
        listlen = len(extractattribute)
        keyInfo = extractattribute[listlen-2]
        if ("font" in keyInfo):
            tempInfo = keyInfo.split("<font")
            lSymbol = tempInfo[0].rfind(">")
            tempEntry = tempInfo[0][lSymbol+1:]
            keyData[attribute] = tempEntry
        else: 
          lSymbol = keyInfo.rfind(">")
          tempEntry = keyInfo[lSymbol+1:]
          keyData[attribute] = tempEntry
   

  #store price of vehicle
  title2 = str(soup.find(class_="large-text buynow-details asking-price-text"))
  if (title2 == "None"):
    price = "Bidding - No Price" #can consider searching for initial bidding price
  else: 
    extractPricePos1 = title2.rfind("</span>")
    extractFull = title2[:extractPricePos1]
    extractPricePos2 = extractFull.rfind(">")
    price = extractFull[extractPricePos2+1:]
  

  #consolidating details 
  model = keyData["Model detail"]
  checkduplicate = brandModel.find(model)
  if (checkduplicate == "-1"):
    keyData["Brand"] = brandModel
  else:
    newModel = brandModel[:checkduplicate-1]
    keyData["Brand"] = newModel

  keyData["Year"] = year
  keyData["Price"] = price
  keyData["Dealer Code"] = dealercode

  return keyData



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
  insert_tuple = []
  for data in singleData:
    insert_tuple.append(singleData[data])

  mycursor.execute(sql, insert_tuple)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")
  dealercode += 1


#Auto run page to generate URL
urltest = "https://www.trademe.co.nz/motors/used-cars/holden/auction-2203458038.htm?rsqid=77406652aa6b40d58b6e1dae8d644e6e-001"


urltest1 = "https://www.trademe.co.nz/motors/used-cars/toyota/auction-2207225515.htm?rsqid=d1a45702bdb144e5b3a24f7efb34ef72-001"

urltest2 = "https://www.trademe.co.nz/motors/used-cars/mercedesbenz/auction-2207776231.htm?rsqid=7b28d9b8e8254592b7031e9ad1330357-001"
singleData = extractdate(urltest, dealercode) 
print(singleData)
#dealer code incomplete --> Require update (Dealer address)

insertintoDB(singleData, dealercode)

