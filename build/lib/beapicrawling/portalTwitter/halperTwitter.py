import requests
import json
import datetime
import hashlib
import urllib.parse
import time
from time import gmtime, strftime
from kafka import KafkaProducer
import happybase
import tweepy
import os

consumer_key = "m1IfyHbaKnpKfq1aUHnSpmWx5"
consumer_secret = "SLKNUIY9PJENSmcIG3YsIdtbvAZAweSvHI4KmeX8FSthQe9nBG"
access_token = "1431351007825444864-eFCWHsziG3jMQzTLbbCh4DfJE5QEMi"
access_token_secret = "38Ezfsxbkd0nqtF0akThVdaAyMZHSHSQW57dEX9pE9EF4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


############################ CONNECTION HOSTS =====
kafkaIp=os.environ.get('kafkaIp')
openSearchIp=os.environ.get('openSearchIp')
openSearchPort=os.environ.get("openSearchPort")
hbaseIp=os.environ.get('hbaseIp')
hbasePort=os.environ.get('hbasePort')
apiPort=os.environ.get("apiPort")
apiIP=os.environ.get('apiIp')
############################ CONNECTION HOSTS =====

class TwitterPorTals():
    def __init__(self,topicID):
        self.config = ""
        self.topic = ""
        self.data=[]
        self.topicID = topicID
    def getConfig(self):
        if self.topicID == "None":
            topic = requests.get("http://"+apiIP+":"+apiPort+"/api/v1/config/crawling/keyword-list")
            self.topic = json.loads(topic.text)
            self.topic = self.topic["data"]
            print("di get topic ================",self.topic)
        else:
            topic = requests.get("http://"+apiIP+":"+apiPort+"/api/v1/config/crawling/keyword-list?topic_id="+self.topicID)
            if topic.status_code != 200:
                return{
                    "message" : "Please check config topic"
                }
            self.topic = json.loads(topic.text)
            self.topic = self.topic["data"]
            print("di get topic ================",self.topic)
            if len(self.topic) == 0:
                return {
                    "message" : "Please check topicid"
                }
        config = requests.get("http://"+apiIP+":"+apiPort+"/api/v1/config/source")
        self.config = json.loads(config.text)
        self.config = self.config["data"]
        print("di get config ================",self.config)
        # path  = __file__
        # splited = path.split("/")
        # path=""
        # for i in splited[1:-2]:
        #     path += "/"+i
        # f = open((path+"/portalBeritaV2/config.json"))
        # data = json.load(f)
        # self.config = data
        ############################################################################
        # path  = __file__
        # splited = path.split("/")
        # path=""
        # for i in splited[1:-2]:
        #     path += "/"+i
        # f = open((path+"/portalBeritaV2/keywordlist.json"))
        # data = json.load(f)
        # self.topic = data
    def doGetTwitte(self,length):
        data = []
        print("masuk get ==================")
        print(self.topic,self.config,"ini-----------")
        for i in self.topic:
            for j in self.config:
                if (j["source"] == "twitter"):
                    print(i["keyword"],i["topics"])
                    tw = tweepy.Cursor(api.search,
                    q=i["keyword"],
                    lang="in",
                    ).items(length)
                    for k in tw:
                        data.append(
                        {
                            "id":k._json["id_str"],
                            "source_url":"",
                            "title": "from twitter",
                            "content":[k._json["text"]],
                            "createdAt":k._json["created_at"],
                            "creator":"twitter",
                            "topic":i["topics"],
                            "keyword": [i["keyword"]],
                            "last_crawled": strftime("%d-%m-%Y %H:%M:%S", gmtime()),
                            "user": k._json["user"]["id_str"],
                            "userinfo": k._json["user"],
                            "page":"",
                            "types":"twitter"
                        }
                        )
        self.data = data
    def doSendKafka(self):
        print("============= MASUK KAFKA")
        data = self.data
        print(" ================= 1")
        # data = self.data
        producer = KafkaProducer(bootstrap_servers=[kafkaIp],
        # value_serializer=lambda m: json.dumps(m).encode('ascii')
        )
        connection = happybase.Connection(hbaseIp,int(hbasePort),transport='framed')
        connection.open()
        table = connection.table('DEV')
        count=0
        print(" ===================== 2",hbaseIp,hbasePort,table)
        for i in data:
            print(i," ini i =============================")
            byte = i["id"].encode('utf-8')
            row = table.row(byte)
            print(row,"============== raw")
            if row:
                for name,dict_ in row.items():
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
                print(self.topicID,"topic id")
                if self.topicID == "None":
                    i["scrap_type"]="None"
                    producer.send('ScrappingDataHBASE',  json.dumps(i).encode('utf-8'))
                    time.sleep(1)
                else:
                    print("disini")
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
        print("================= SEND TWITTER DATA TO KAFKA =====================")