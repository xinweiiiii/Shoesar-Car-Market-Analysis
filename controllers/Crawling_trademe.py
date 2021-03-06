import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

#Trade me
def getnextpage(url, count): #Extract the url for next page
  posNo1 = url.find("page") 
  front = url[:posNo1+5]
  posNo2 = url.rfind("&")
  back = url[posNo2:]
  
  pageNumber = url[posNo1+5:posNo2]
  newPageNumber = int(pageNumber) + count
  
  return front + str(newPageNumber) + back
  
  
def mainpageextractionurl(main_url): #extract all the car detail url from a page and store into a list
  page = urllib.request.urlopen(main_url)
  soup = BeautifulSoup(page,features="html.parser")
  allref = soup.find_all(class_="tmm-sf-search-card-list-view__link")
  tempurl = []
  for singleurl in allref:
    singleurl = str(singleurl)
    pos1 = singleurl.find("href=")
    pos2 = singleurl.find(">")
    newlink = singleurl [pos1+6:pos2-1]
    if (newlink not in tempurl):
      tempurl.append(newlink)
  return tempurl


def extractdate(url, dealercode): #extracting information from a single url

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
  if (brandModelyear[0].isdigit()):
    extractyear = brandModelyear.find(" ")
    year = brandModelyear[:extractyear]
    brandModel = brandModelyear[extractyear+1:]
  else:
    extractyear = brandModelyear.rfind(" ")
    year = brandModelyear[extractyear+1:]
    brandModel = brandModelyear[:extractyear]
  
  getBrand = brandModel.find(" ")
  brandFinal = brandModel[:getBrand]
  modelAndDetail = brandModel[getBrand:]



  #store all the car information for keydetail section
  title1 = str(soup.find_all(class_="attributes-box key-details-box"))
  allKeyDetails = title1.split("</li>")
  
  keyAttribute = ["Number plate", "Kilometres", "Engine size", "Transmission"]
  
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
  checkduplicate = modelAndDetail.find(model)
  if (checkduplicate == "-1"):
    keyData["Model detail"] = modelAndDetail
  else:
    newModel = modelAndDetail[:checkduplicate-1]
    keyData["Model detail"] = newModel

  keyData["Year"] = int(year)
  keyData["Price"] = price
  keyData["Dealer Code"] = int(dealercode)
  keyData["Brand"] = brandFinal
  

  if (keyData["Number plate"] == ""):
    newCarPlate = getrandomcarplate()
    keyData["Number plate"] = newCarPlate

  if (keyData["Number plate"] in currentNumber):
    numberplatev1 = keyData["Number plate"]
    numberplatev2 = numberplatev1 + "(duplicate)"
    keyData["Number plate"] = numberplatev2
    
  
  currentNumber.append(keyData["Number plate"])
  

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


def insertintoDB(singleData, dealercode): #Storing into the database
  import mysql.connector
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="shoesarcar"
  )

  mycursor = mydb.cursor()
  sql =  " INSERT INTO trademecarinfo (carplatenumber, brand, model, yearofmanufactured, milleage, price, transmission,dealercode,enginecapacity) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
  insert_tuple = []
  for data in singleData:
    insert_tuple.append(singleData[data])

  mycursor.execute(sql, insert_tuple)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")



#Run Main Code
main_url = "https://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?searchregion=100&cid=268&search=1&nofilters=1&originalsidebar=1&rptpath=1-268-&rsqid=fb59e7ae3bce42079331e5668d043b93-006&key=776208965&page=1&sort_order=mtr_best_match"
dealercode = 1
tempcount = 0
currentNumber = []
for i in range (0,10000):
  urlSingle = getnextpage(main_url,i)
  pageAll = mainpageextractionurl(urlSingle)
  for url in pageAll:
    tempcount += 1
    newurl = "https://www.trademe.co.nz/motors/used-cars" + url
    singleData = extractdate(newurl, dealercode) 
    insertintoDB(singleData, dealercode)
    dealercode+=1
print(tempcount)










