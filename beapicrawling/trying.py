# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1420,1080')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

# ############################################################ DETIK COM ##########################################################
# driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
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

# import happybase
# connection = happybase.Connection("172.16.28.11",9090,transport='framed')
# connection.open()
# # table = connection.table('DEV')
# # row = table.row()
# print(connection.tables())
# connection.close()

# from kafka import KafkaConsumer
# consumer =  KafkaConsumer('ScrappingDataHBASEOne',bootstrap_servers='almidekod01.tnial.intern:6667')
# for i in consumer:
#     print(i)

# l = [{'a': 123, 'b': 1234},
#         {'a': 3222, 'b': 1234},
#         {'a': 123, 'b': 1234}]

# seen = set()
# new_l = []
# for d in l:
#     t = tuple(d.items())
#     if t not in seen:
#         seen.add(t)
#         new_l.append(d)

# print(new_l)

import requests
import json
apiIP="192.168.10.18"
apiPort="4008"
payload = json.dumps({"id_setting": 5})
headers = {"Content-Type":"application/json",
"Authorization": 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI5ZXVnbnItZER1djF0WEVpMzBjbUVtRUJuTjhva0lRc0NmTWFWa3dxSEFRIn0.eyJleHAiOjE2NjU1NjgyMTAsImlhdCI6MTY2Mjk3NjIxMCwianRpIjoiZTQ2NWM4ZGItMGIyZi00MmM5LWJjNTMtMjgwOGI3OGZiOWVjIiwiaXNzIjoiaHR0cHM6Ly8xOTIuMTY4LjEwLjE4Ojg0NDMvYXV0aC9yZWFsbXMvT3BlblNlYXJjaFRlc3RLZXljbG9hayIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI3NDA3ZDFmNS0wMTllLTRlNjAtYmQ4My1mMDc0ODczZjE5ZWMiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJTU08tQUwiLCJzZXNzaW9uX3N0YXRlIjoiZTQ1NWVhNzUtMmUxZi00MzUzLWEwYWUtNTJkOWE0MDJjYmFjIiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW9wZW5zZWFyY2h0ZXN0a2V5Y2xvYWsiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiYXBwLXVzZXIiXX0sInJlc291cmNlX2FjY2VzcyI6eyJTU08tQUwiOnsicm9sZXMiOlsiVXNlciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJhZGRyZXNzIG9mZmxpbmVfYWNjZXNzIG1pY3JvcHJvZmlsZS1qd3QgcGhvbmUgZW1haWwgcHJvZmlsZSIsInNpZCI6ImU0NTVlYTc1LTJlMWYtNDM1My1hMGFlLTUyZDlhNDAyY2JhYyIsInVwbiI6InN5YXJpZiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiYWRkcmVzcyI6e30sIm5hbWUiOiJTeWFyaWYgSGlkYXlhdCIsImdyb3VwcyI6WyJkZWZhdWx0LXJvbGVzLW9wZW5zZWFyY2h0ZXN0a2V5Y2xvYWsiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiYXBwLXVzZXIiXSwicHJlZmVycmVkX3VzZXJuYW1lIjoic3lhcmlmIiwiZ2l2ZW5fbmFtZSI6IlN5YXJpZiIsImZhbWlseV9uYW1lIjoiSGlkYXlhdCIsImVtYWlsIjoic3lhcmlmaGlkYXlhdDQwMEBnbWFpbC5jb20ifQ.FDnLlC5G2CQ7PVyBlFtImUt90aNR4Ooi7CrUHcd3-1H94gp_BnH7NWW1dCSBZkvh4R_vnPl3VsH-ByIeHsv-cBRb8hzW_p0L25qfbIQJJigq4-b3Wi5r5QuBZ7nXRkiXgZufy4QIEQTq9Dr_MtEkrXzbhl0BZzH-HVY0jk-aQhyDwik_YtaYf0AlJmjpwQffzJz9KNKGkF1Ct5Iy7Gmo5pnj2WkwpI7Qq5AV41PdxGAUSe7JpZijsetHAIfE1y3RKmVcsWxj0xcvpLE0nt6luYqiQUW-ukaCivo9wzjo26SgGp0xPhvHyeqE0PdtzNP8K-3URFV4EBD0m6ak_meh0A' }
response = requests.request("POST", url="http://"+apiIP+":"+apiPort+"/api/v1/log-setting", headers=headers, data=payload)

print(response.text)
