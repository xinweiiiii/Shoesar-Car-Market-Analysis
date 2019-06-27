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

 #store all the car information
cleandetail = []
for entry in cardetail:
    lsymbol = entry.find(">")
    tempentry = entry[lsymbol:]
    rsymbol = tempentry.find("<")
    newentry = tempentry[1:rsymbol]
    cleandetail.append(newentry)
print(cleandetail)


# import mysql.connector
# from mysql.connector import Error
# from mysql.connector import errorcode
# try:
#    connection = mysql.connector.connect(host='localhost',
#                              database='',
#                              user='root',
#                              password='shoesarcar')
#    sql_insert_query = """ INSERT INTO `carinfo`
#                           (`carplatenumber`, `brand`, `model`, `yearofmanufactured`,'milleage', 'price', 'transmission','dealercode','enginecapacity') VALUES ('SBJ1628G','Mercedes','C180', '2019','2000KM','Auto','0001','1600')"""
#    cursor = connection.cursor()
#    result  = cursor.execute(sql_insert_query)
#    connection.commit()
#    print ("Record inserted successfully into python_users table")
# except mysql.connector.Error as error :
#     connection.rollback() #rollback if any exception occured
#     print("Failed inserting record into python_users table {}".format(error))
# finally:
#     #closing database connection.
#     if(connection.is_connected()):
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="shoesarcar"
)

mycursor = mydb.cursor()
sql =  " INSERT INTO carinfo (carplatenumber, brand, model, yearofmanufactured, milleage, price, transmission,dealercode,enginecapacity) VALUES (cleandetail[0], 'cleandetail[2]','cleandetail[7]', 2019 ,'cleandetail[1]','150000','cleandetail[6]','0001','1600')"
mycursor.execute(sql)

mydb.commit()

print(mycursor.rowcount, "record inserted.")




