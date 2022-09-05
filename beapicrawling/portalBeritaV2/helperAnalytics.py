from site import venv
import requests
import json
from bs4 import BeautifulSoup
import re
import datetime
import hashlib
import urllib.parse
import time
from time import gmtime, strftime
from portalBeritaV2.seleniumed import Seleniumed
from kafka import KafkaProducer
import happybase
from opensearchpy import OpenSearch
import os

# test =  os.environ.get('hbasePort')
kafkaIp=os.environ.get('kafkaIp')
openSearchIp=os.environ.get('opensearchIp')
hbaseIp=os.environ.get('hbaseIp')
hbasePort=os.environ.get('hbasePort')
apiPort=os.environ.get("apiPort")
apiIP=os.environ.get('apiIP')
print(kafkaIp,openSearchIp,hbaseIp,hbasePort,apiPort,apiIP)
class Helper():
    def __init__(self,topicId):
        self.config = ""
        self.topic = ""
        self.endPoint = "http://"+apiIP+":"+apiPort+"/api/v1/config/crawling"
        self.whitelist=[]
        self.detailsCrawl=[]
        self.data = []
        self.selenium = Seleniumed()
        self.topicId = topicId
    def getConfig(self):
        try:
            if self.topicId == "None":
                topic = requests.get("http://"+apiIP+":"+apiPort+"/api/v1/config/crawling/keyword-list")
                self.topic = json.loads(topic.text)
                self.topic = self.topic["data"]
            else:
                topic = requests.get("http://"+apiIP+":"+apiPort+"/api/v1/config/crawling/keyword-list?topic_id="+self.topicId)
                if topic.status_code != 200:
                    return {
                        "message" : "please check topic config"
                    }
                self.topic = json.loads(topic.text)
                self.topic = self.topic["data"]
                if len(self.topic) == 0:
                    return {
                        "message" : "please check topicID"
                    }
            config = requests.get("http://"+apiIP+":"+apiPort+"/api/v1/config/source")
            self.config = json.loads(config.text)
            self.config = self.config["data"]
            ######################DELET THIS JIKA SUDAH SIAP EAAAA######################
            # path  = __file__
            # splited = path.split("/")
            # path=""
            # for i in splited[1:-1]:
            #     path += "/"+i
            # f = open((path+"/config.json"))
            # data = json.load(f)
            # self.config = data
            ###########################################################################
            # path  = __file__
            # splited = path.split("/")
            # path=""
            # for i in splited[1:-1]:
            #     path += "/"+i
            # f = open((path+"/keywordlist.json"))
            # data = json.load(f)
            # self.topic = data
            ######################## UNCOMMAND YG DIBAWAH YAAA #######################
            
            
        except BaseException as err:
            print(str(err))
    def doScrapLink(self):
        for i in self.topic:
            # i["topics"].append(i["keyword"])
            for j in self.config:
                count = 1
                for k in range(int(j["crawl_deep"])):
                    if (j["source"] != "twitter"):
                        # print(j["base_url"],i["keyword"],count)
                        # r = requests.get(str(j["base_url"])+urllib.parse.quote_plus(i["keyword"])+"&page="+str(count))
                        # print("=====================RES",r.status_code)
                        # soup = BeautifulSoup(r.content,"html.parser")
                        # value = soup.findAll('a',href=True)
                        value = self.selenium.doGetLinkUsingSelenium(j["base_url"],i["keyword"],count,j["source"],j["returnLink"])
                        for k in value:
                            self.FilterWhiteList(k,i,j,count)
                        count+=1
    def halperDuplicateData(self,newdata):
        for i in self.data:
            if i["source_url"] == newdata:
                return True
        return False
    def FilterBlacklist(self,splitedUrl,blacklist):
        for k in blacklist:
            splitedBlacklist = k.split("/")
            print("=================================== INI ",splitedUrl[3],splitedBlacklist[1])
            if splitedUrl[2] == splitedBlacklist[0] and splitedUrl[3] == splitedBlacklist[1]:
                return True
        return False
    def FilterWhiteList(self,link,topic,config,page):
        try:
            topics = topic
            splitedLink = link.split("/")
            print("============================= 1",splitedLink)
            if(len(splitedLink)>4 and splitedLink):
                print("============================= 2")
                for j in config["white_list"]:
                    print("============================= 3")
                    white_list = j.split("/")
                    print("============================= 4",white_list,splitedLink)
                    # print(splitedLink[2],"========================== LINK")
                    # if(splitedLink[2] =="m.antaranews.com"):
                    #     print(splitedLink[2],"========================== LINK")
                    if(white_list[0] == splitedLink[2]):
                        print("============================= 5")
                        # print(splitedLink[2],"========================== LINK")
                        blacklisted = self.FilterBlacklist(splitedLink, config["black_list"])
                        isDuplicate = self.halperDuplicateData(link)
                        print("============================= 6")
                        if blacklisted == False and isDuplicate == False:
                            print("============================= 7")
                            # print(link,config["black_list"],blacklisted,"============================ WHITELIST FILTER")
                            title = self.getTitle(link)
                            print("============================= 8")
                            # print(title,"============================ TITTLE")
                            # topic["topics"].append(topic["keyword"])
                            self.data.append({
                                    "id":hashlib.md5(link.encode('utf-8')).hexdigest(),
                                    # "id":link,
                                    "source_url":link,
                                    "title": title,
                                    "content":[],
                                    "createdAt":"",
                                    "creator":config["source"],
                                    "topic":topic["topics"],
                                    "keyword": [topic["keyword"]],
                                    "tagContent" : config["tagContent"],
                                    "tagTime" : config["tagTime"],
                                    "last_crawled": strftime("%d-%m-%Y %H:%M:%S", gmtime()),
                                    "types":"news",
                                    "page":str(page),
                                    "user" : "",
                                    "userinfo":{}
                                })
        except BaseException as err:
            print(str(err))
            pass
    def getTitle(self,link):
        try:
            newlink = link.split("/")
            newlink = newlink[-1]
            return newlink.replace("-", " ")
        except BaseException as err:
            pass
    def dogetContets(self):
        data = self.data
        for k in data:
            url = k["source_url"]
            r = requests.get(url)
            soup = BeautifulSoup(r.content,"html.parser")
            # value = soup.findAll('p')
            value = soup.findAll(k["tagContent"]["item"],k["tagContent"]["value"])
            time = soup.findAll(k["tagTime"]["item"],k["tagTime"]["value"])
            titleUpdate = soup.find("title")
            text = []
            resultTime = ""
            for i in value:
                stringText = re.sub(r'[-()\"#/@;:\n\t-=~|.?,]'," ",str(i.get_text()))
                if len(stringText) > 2:
                    text.append(stringText)
            for i in time:
                stringText = str(i.get_text())
                resultTime = stringText
            if(k["creator"] == "antaranews"):
                resultTime = time[0].text
            if len(text) == 0:
                k["invalid_content"] = True
            else:
                k["invalid_content"] = False
            k["content"]=text
            k["createdAt"] = resultTime
            k["title"] = titleUpdate.text
            del k["tagTime"]
            del k["tagContent"]
        self.data = data
    def doSendKafka(self):
        count = 0
        data = self.data
        producer = KafkaProducer(bootstrap_servers=[kafkaIp],
        # value_serializer=lambda m: json.dumps(m).encode('ascii')
        )
        connection = happybase.Connection(hbaseIp,int(hbasePort),autoconnect=False)
        connection.open()
        table = connection.table('DEV')
        for i in data:
            byte = i["id"].encode('utf-8')
            row = table.row(byte)
            if row:
                for name,dict_ in row.items():
                    print("======== k3")
                    stringed = name.decode("utf-8") 
                    if stringed == "NEWS:keyword":
                        nowKeyword = i["keyword"][0]
                        print(stringed,dict_.decode("utf-8"))
                        dictStr = dict_.decode("utf-8")
                        print(type(json.loads(dictStr)))
                        i["keyword"] = json.loads(dictStr)
                        i["keyword"].append(nowKeyword)
                        i["keyword"]=list(dict.fromkeys(i["keyword"]))
            try:
                print(json.dumps(i).encode('utf-8'),"===============kafka data")
                if self.topicId == "None":
                    print("masuk ALL ========================")
                    i["scrap_type"]="None"
                    producer.send('ScrappingDataHBASE',  json.dumps(i).encode('utf-8'))
                    time.sleep(1)
                else:
                    print("masuk ONE ========================")
                    i["scrap_type"]="One"
                    producer.send('ScrappingDataHBASEOne',  json.dumps(i).encode('utf-8'))
                    time.sleep(1)
                # producer.send('ScrappingDataOpensearch', json.dumps(i).encode('utf-8'))
                # time.sleep(1)
                # producer.close()
                count+=1
                print("emited",count)
            except BaseException as err:
                print(err,"=========================")
        connection.close()
        producer.close()
        count = 0
        print(len(data),"len data")
        print("================= SEND ALL CRAWLING DATA TO KAFKA =====================")
