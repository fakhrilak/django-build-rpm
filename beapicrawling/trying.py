from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

############################################################ DETIK COM ##########################################################
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
# driver.get("https://www.detik.com/search/searchall?query=TNI AL Gilimanuk&page=1")
# elem = driver.find_elements(by=By.TAG_NAME,value='a')
# data= []
# count = 0
# for i in elem:
#     try:
#         link = i.get_attribute("href").split("/")
#         if len(link) > 3:
#             data.append(i.get_attribute("href"))
#         count+=1
#     except BaseException as err:
#         print(err)
# print(data[49:58])
# driver.close()
############################################################ KOMPAS #############################################################
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
# driver.get("https://search.kompas.com/search/?q=jokowi")
# elem = driver.find_elements(by=By.TAG_NAME,value='a')
# data= []
# count = 0
# def double(data,array):
#     for j in array:
#         if j == data:
#             return False
#     return True
# for i in elem:
#     try:
#         link = i.get_attribute("href").split("/")
#         if len(link) > 3:
#             a = double(i.get_attribute("href"),data)
#             print(a)
#             if link[3] == "read" and a == True:
#                 data.append(i.get_attribute("href"))
#         count+=1
#     except BaseException as err:
#         print(err)
# print(data[:-2])
# driver.close()
#########################################################CNN INDONESIA############################################################
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
# driver.get("https://www.cnnindonesia.com/search/?query=TNI AL Gilimanuk&page=1")
# elem = driver.find_elements(by=By.TAG_NAME,value='a')
# data= []
# count = 0
# for i in elem:
#     # link = i.get_attribute("href").split("/")
#     # if link[3] == "berita":
#     data.append(i.get_attribute("href"))
#     count+=1
# print(data[83:93])
# driver.close()
########################################################ANTARA NEWS################################################################
# def validate(title):
#     for j in title:
#         if j == "?":
#             return True
#     return False
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
# driver.get("https://www.antaranews.com/search/jokowi/1?q=jokowi")
# elem = driver.find_elements(by=By.TAG_NAME,value='a')
# cou = 0
# data= []
# for i in elem:
#     link = i.get_attribute("href")
#     query = validate(link)
#     if query == False:
#         data.append(link)
#         # print(link,cou)
#         cou+=1
# # print(data)
# batas = data[108].split("/")
# # print(data,len(data))
# if(batas[3]!= "berita"):
#     print("not found berita")
# else:
#     print("ada nich")
#     print(data[108:171])
# # print(data[416:478])
# driver.close()

# import requests
# import json
# from bs4 import BeautifulSoup
# r = requests.get("https://www.antaranews.com/berita/2323162/kemenhub-tni-al-gelar-vaksinasi-di-pelabuhan-ketapang-jatim")
# soup = BeautifulSoup(r.content,"html.parser")
# # value = soup.findAll('p')
# titleUpdate = soup.findAll("span",{"class":"article-date"})
# print(titleUpdate[0].text)
# for i in titleUpdate:
#     print(i.text)

import happybase
connection = happybase.Connection("192.168.10.110",9093,autoconnect=False)
connection.open()
table = connection.table('DEV')
row = table.row()
print(row)