from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


def getAllPageUrl(startingurl):
  req = Request(startingurl, headers={'User-Agent': 'Mozilla/5.0'})
  page = urlopen(req).read()
  soup = BeautifulSoup(page,features="html.parser")
  mainref = str(soup.find_all(class_="aacf-listing"))
  allurl = mainref.split("href")
  allurl.pop(0)
  urlarray = []
  for oneUrl in allurl:
    findFirstPos = oneUrl.find("<img")
    if (findFirstPos > 0):
      getlink = oneUrl[2:findFirstPos-3]
      if (getlink not in urlarray):
        urlarray.append(getlink)

  return urlarray 

def mainpageextractionurl(main_url, dealercode):
  req = Request(main_url, headers={'User-Agent': 'Mozilla/5.0'})
  page1 = urlopen(req).read()
  soup = BeautifulSoup(page1,features="html.parser")

  keyData = {"Number plate": "", "Brand": "","Model detail": "","Year":"", "Kilometres": "", "Price": "", "Transmission": "", "Dealer Code": "", "Engine size": "" }

  #Price
  priceref = str(soup.find_all(class_="right-block"))
  pricePos1 = priceref.find("</small>")
  pricePos2 = priceref.rfind("</h2>")
  price = priceref[pricePos1+8:pricePos2]
  keyData["Price"] = price

  dataref = str(soup.find_all(class_="vehicle-attribute-wrapper"))
  categorizedataref = dataref.split("<li>")
  for data in categorizedataref:
    #Brand
    if ("Make" in data):
      makePos1 = data.find("<span>")
      makePos2 = data.rfind("</span>")
      make = data[makePos1+6:makePos2]
      keyData["Brand"] = make
    #model
    if ("Model" in data):
      modelPos1 = data.find("<span>")
      modelPos2 = data.rfind("</span>")
      model = data[modelPos1+6:modelPos2]
      keyData["Model detail"] = model
    #year
    if ("Year" in data):
      yearPos1 = data.find("<span>")
      year = data[yearPos1+6:yearPos1+10]
      keyData["Year"] = year
    #Kilometers
    if ("Odometer" in data):
      milleagePos1 = data.find("<span>")
      milleagePos2 = data.rfind("</span>")
      milleage = data[milleagePos1+6:milleagePos2]
      keyData["Kilometres"] = milleage
    #Transmission
    if ("Transmission" in data):
      transmissionPos1 = data.find("<span>")
      transmissionPos2 = data.rfind("</span>")
      transmission = data[transmissionPos1+6:transmissionPos2]
      keyData["Transmission"] = transmission
    #enginesize 
    if ("CC Rating" in data):
      enginePos1 = data.find("<span>")
      enginePos2 = data.rfind("</span>")
      enginesize = data[enginePos1+6:enginePos2]
      keyData["Engine size"] = enginesize


  newCarPlate = getrandomcarplate()
  keyData["Number plate"] = newCarPlate
  currentNumber.append(keyData["Number plate"])

  dealercode += 1
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



currentNumber = []
dealercode = 0
resulturl = getAllPageUrl("https://www.aa.co.nz/cars/cars-for-sale/?start=0")
for urlOne in resulturl:
  tempurl = "https://www.aa.co.nz" + urlOne 
  temp = mainpageextractionurl(tempurl, dealercode)
  print(temp)
  dealercode += 1

