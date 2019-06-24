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


# temptitle = titleref[2].rstrip("</a")
# label = []
# label.append(temptitle)

# data = []
# overalldata = []
# table = soup.find_all("tr")[3]
# depreciation = table.find_all(class_="row_info")
# for i in depreciation:
#     for temp in i:
#         result = ""
#         for letter in temp:
#             if letter != " " and letter != "\r" and letter != "\t" and letter != "\n":
#                 result += letter
#         data.append(result)
# del data[2:5]
# del data[7:9]
# overalldata.append(data)


# df = pd.DataFrame(overalldata, columns = ["Mileage","Road Tax","COE","Engine Capacity","Weight","Manufactured Year","Transmission","Power","No of Owners"], index = label)
# print(df)



