from itertools import count
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
chrome_options.add_argument('--disable-dev-shm-usage')   

class Seleniumed():
    def __init__(self):
        pass
    def doGetLinkUsingSelenium(self,link,keywords,page,portalBerita,returnLink):
        try:
            data = []
            if portalBerita == "antaranews":
                try:
                    def validate(title):
                        for j in title:
                            if j == "?":
                                return True
                        return False
                    print("===================== ANTARA NEWS ========================",page,"https://www.antaranews.com/search?q="+keywords)
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
                    if page == 1:
                        driver.get("https://www.antaranews.com/search?q="+keywords)
                    else:
                        driver.get("https://www.antaranews.com/search/"+keywords+"/"+str(page)+"?q="+keywords)
                    # driver.get("https://www.antaranews.com/search/jokowi/2?q=jokowi")
                    elem = driver.find_elements(by=By.TAG_NAME,value='a')
                    cou = 0
                    data= []
                    for i in elem:
                        link = i.get_attribute("href")
                        query = validate(link)
                        if query == False:
                            data.append(link)
                            cou+=1
                    driver.close()
                    batas = data[108].split("/")
                    if(batas[3]!= "berita"):
                        return []
                    else:
                        print("ada nich")
                        print(data[108:171])
                        return data[returnLink["start"]:returnLink["end"]]
                except BaseException as err :
                    print(" ================== ERROR INDEX",str(err))
                    return[]
            elif portalBerita == "detik":
                try:
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
                    driver.get("https://www.detik.com/search/searchall?query="+keywords+"&pages="+str(page))
                    elem = driver.find_elements(by=By.TAG_NAME,value='a')
                    data= []
                    count = 0
                    for i in elem:
                        try:
                            link = i.get_attribute("href").split("/")
                            if len(link) > 3:
                                data.append(i.get_attribute("href"))
                            count+=1
                        except BaseException as err:
                            print(err)
                    print(data[returnLink["start"]:returnLink["end"]])
                    driver.close()
                    return data[returnLink["start"]:returnLink["end"]]
                except BaseException as err:
                    print("================= ERROR DI INDEX ",str(err))
                    return []
            elif portalBerita == "kompas":
                try:
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
                    driver.get("https://search.kompas.com/search/?q="+keywords+"page="+str(page))
                    elem = driver.find_elements(by=By.TAG_NAME,value='a')
                    data= []
                    count = 0
                    def double(data,array):
                        for j in array:
                            if j == data:
                                return False
                        return True
                    for i in elem:
                        try:
                            link = i.get_attribute("href").split("/")
                            if len(link) > 3:
                                a = double(i.get_attribute("href"),data)
                                if link[3] == "read" and a == True:
                                    data.append(i.get_attribute("href"))
                            count+=1
                        except BaseException as err:
                            print(err)
                    print(data[returnLink["start"]:returnLink["end"]])
                    driver.close()
                    return data[returnLink["start"]:returnLink["end"]]
                except BaseException as err:
                    print("================= ERROR DI INDEX ",str(err))
                    return []
            elif portalBerita == "cnnindonesia":
                try:
                    print("===================== CNN INDONESIA ========================")
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
                    driver.get("https://www.cnnindonesia.com/search/?query="+keywords+"&pages="+str(page))
                    elem = driver.find_elements(by=By.TAG_NAME,value='a')
                    data= []
                    count = 0
                    for i in elem:
                        # link = i.get_attribute("href").split("/")
                        # if link[3] == "berita":
                        data.append(i.get_attribute("href"))
                        count+=1
                    print(data[returnLink["start"]:returnLink["end"]])
                    driver.close()
                    return data[returnLink["start"]:returnLink["end"]]
                except BaseException as err:
                    print("======================= ERROR DI INDEX ",str(err))
                    return []
        except BaseException as err:
            print("============================= ERROR DI SELENIUM =")
            return []