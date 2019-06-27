import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url = "https://www.trademe.co.nz/motors/used-cars/holden/auction-2203458038.htm?rsqid=77406652aa6b40d58b6e1dae8d644e6e-001"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page)

title = str(soup.find_all(class_="motors-attribute-value"))
cardetail = title.split("</span>")
print(cardetail)
#store all the car information
cleandetail = []
for entry in cardetail:
    lsymbol = entry.find(">")
    tempentry = entry[lsymbol+1:]
    checkforsymbol = tempentry.find("<")
    if (checkforsymbol != -1):
      tempentry = tempentry[:checkforsymbol]
    if (tempentry != ""):
      cleandetail.append(tempentry)
print(cleandetail)




#DB Testing
# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="",
#   database="shoesarcar"
# )

# mycursor = mydb.cursor()
# sql =  " INSERT INTO carinfo (carplatenumber, brand, model, yearofmanufactured, milleage, price, transmission,dealercode,enginecapacity) VALUES (cleandetail[0], 'cleandetail[2]','cleandetail[7]', 2019 ,'cleandetail[1]','150000','cleandetail[6]','0001','1600')"
# mycursor.execute(sql)

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")




