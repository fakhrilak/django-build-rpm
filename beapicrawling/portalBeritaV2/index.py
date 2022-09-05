from ninja import Router
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import happybase
import uuid
import time
from ninja import Schema
from portalBeritaV2.helperAnalytics import Helper as helperAnalytics
from opensearchpy import OpenSearch
import os
router = Router()

kafkaIp=os.environ.get('kafkaIp')
openSearchIp=os.environ.get('opensearchIp')
openSearchPort=os.environ.get("openSearchPort")
hbaseIp=os.environ.get('hbaseIp')
hbasePort=os.environ.get('hbasePort')
apiPort=os.environ.get("apiPort")
apiIP=os.environ.get('apiIP')

@router.get("/news")
def getCrawling(request,content:bool,kafka:bool,topicId:str):
    try:
        analyticst = helperAnalytics(topicId)
        analyticst.getConfig()
        analyticst.doScrapLink()
        time.sleep(2)
        if content == True:
            analyticst.dogetContets()
        if kafka == True:
            analyticst.doSendKafka()
        return {
                "message" : "Success",
                "data" :  analyticst.data
                # "config" : analyticst.config,
                # "topic"  : analyticst.topic
            }
    except BaseException as err:
        return {
            "message" : str(err)
        }

class NewsScema(Schema):
    content:bool
    kafka: bool
    topicId: str

@router.post("/news")
def Crawling(request,data:NewsScema):
    try:
        analyticst = helperAnalytics(data.topicId)
        analyticst.getConfig()
        analyticst.doScrapLink()
        time.sleep(2)
        if data.content == True:
            analyticst.dogetContets()
        if data.kafka == True:
            analyticst.doSendKafka()
        return {
                "message" : "Success",
                "data" :  analyticst.data
                # "config" : analyticst.config,
                # "topic"  : analyticst.topic
            }
    except BaseException as err:
        return {
            "message" : str(err)
        }
@router.get("/hbaseid/")
def getdataHbaseId(request,id:str):
    try:
        connection = happybase.Connection(hbaseIp,int(hbasePort),autoconnect=False)
        connection.open()
        table = connection.table('DEV')
        byte = id.encode('utf-8')
        row = table.row(byte)
        connection.close()
        if row:
            # print("sudah ada")
            print(row)
            i = {}
            for name,dict_ in row.items():
                print(name,type(dict_))
                # strDict = json.dumps(dict_.decode("utf-8"))
                i[name.decode("utf-8")] = json.loads(json.dumps(dict_.decode("utf-8")).replace('\'', ''))
            return{
                "message" :"succes",
                "data":i
            }
        else:
            return{
                "message" : "data ini belum ada di hbase"
            }
    except BaseException as err:
        print(str(err))
        return{
            "message" :str(err)
        }
@router.get("/openseacrhid")
def getDataOpenSearchById(request,id:str,index:str):
    client = OpenSearch("http://admin:admin@"+openSearchIp+":"+str(openSearchPort))
    result = client.search(
    index=index,
    body={
        "query": {
            "match": {
                "_id":id
                }
            }
        }
    )
    client.close()
    return {
        "data" : result["hits"]["hits"][0]
    }