from ninja import Router
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import happybase
import uuid
from kafka import KafkaProducer
import time
import os


kafkaIp=os.environ.get('kafkaIp')
openSearchIp=os.environ.get('opensearchIp')
hbaseIp=os.environ.get('hbaseIp')
hbasePort=os.environ.get('hbasePort')
apiPort=os.environ.get("apiPort")
apiIP=os.environ.get('apiIP')

producer = KafkaProducer(bootstrap_servers=[kafkaIp],
# value_serializer=lambda m: json.dumps(m).encode('ascii')
)
router = Router()

@router.get("/news")
def portalBerita(request):
    try:
        count = 0
        dataconfig = {
            "url":[
                {
                    "link":"www.kompas.com",
                    "filterItem":[
                        {
                            "index" : 3,
                            "world" : "read"
                        }
                    ],
                    "typedata" : {
                        "item" : "div",
                        "value" : {"" : ""}
                    }
                },
                # {
                #     "link" : "www.antaranews.com",
                #     "filterItem" : [
                #         {
                #             "index" : 3,
                #             "world" : "berita"
                #         }
                #     ],
                #     "typedata" : {
                #         "item" : "div",
                #         "value" : {"class" : "post-content clearfix"}
                #     }
                # },
                {
                    "link" : "www.cnnindonesia.com",
                    "filterItem": [
                        {
                            "index" : 3,
                            "world" : "nasional"
                        }
                    ],
                    "typedata" : {
                        "item" : "p",
                        "value" : {"" : ""}
                    }
                },
                {
                    "link" : "www.detik.com",
                    "filterItem": [
                        {
                            "index" : 3,
                            "world" : "berita"
                        }
                    ],
                    "typedata" : {
                        "item" : "p",
                        "value" : {"" : ""}
                    }
                }
            ],
            "globalFilter":[
                {
                    "world" : "listrik"
                },
                {
                    "world" : "jokowi"
                },
                {
                    "world" : "pembeli"
                }
            ]
        }
        
        data = []
        ############################### PROSES PENGAMBILAN JUDUL BERDASARKAN DATA FILTER ###################################
        for k in dataconfig["url"]:
            r = requests.get("https://"+k["link"])
            soup = BeautifulSoup(r.content,"html.parser")
            # value = soup.findAll('h2',attrs={"class","title"})
            value = soup.findAll('a',href=True)
            for i in value:
                try:
                    splited = i['href'].split("/")
                    title = splited[len(splited)-1]
                    splitedTitle = splited[len(splited)-1].split("-")
                    # print(title)
                    # print("masuk sini",count)
                    if(len(splitedTitle) > 2):
                        statusIndividual = IndividualVilter(splited, k["filterItem"])
                        if statusIndividual== False:
                            statusContents = FilterContents(splitedTitle,dataconfig["globalFilter"])
                            print("/////////////////////////////////////////////////////////////////////////")
                            print("============================== TITLE ",title)
                            if statusContents["status"] == True:
                                statusValidatingData = ValidatingSameData(data, title)
                                if statusValidatingData == False:
                                    data.append({
                                    "link":i['href'],
                                    "title": title,
                                    "content":[],
                                    "createdAt":datetime.now().strftime("%d/%M/%y"),
                                    "sourch_name":k["link"],
                                    "topic":"",
                                    "keyword": statusContents["keyword"],
                                    "typedata":k["typedata"]
                                    })    
                            print("///////////////////////////////////////////////////////////////////////////")
                except BaseException as err:
                    print(err)
        ############################### PROSES CLEANSING DARI LAMBANG YANG TIDAK JELAS ###################################
        for k in data:
            url = k["link"]
            r = requests.get(url)
            soup = BeautifulSoup(r.content,"html.parser")
            # value = soup.findAll('div', {'class': 'post-content clearfix'})
            value = soup.findAll(k["typedata"]["item"],k["typedata"]["value"])
            text = []
            # print(re.sub(r'[-()\"#/@;:\n-=~|.?,]'," ",value))
            for i in value:
                    stringText = re.sub(r'[-()\"#/@;:\n\t-=~|.?,]'," ",str(i.get_text()))
                    if len(stringText) > 2:
                        text.append(stringText)
            k["content"]=text
        countA = 0
        ############################### PROSES ANALYTICS PERHITUNGAN SENTIMENT ###################################
        for i in data:
            # result = CountTopik(dataconfig["globalFilter"], i["content"])
            data[countA].pop("typedata")
            # data[countA]["sentimen"] = result
            countA+=1
        
        # connection = happybase.Connection('192.168.10.191', 8990)
        # table = connection.table('sampleTable')
        for i in data:
            # i["id"] = uuid.uuid4().hex
            i["id"] = i["link"]
            producer.send('testing',  json.dumps(i).encode('utf-8'))
            time.sleep(1)
            # producer.send('error-put',  json.dumps(i).encode('utf-8'))
            # time.sleep(1)
            # table.put(i["link"], {'cf:'+i["link"]: json.dumps(i)})
        # connection.close()
        return {
            "message" : "Success",
            "data" : data,
        }
    except BaseException as err:
        print(str(err))
        return {
            "message" : str(err)
        }

def FilterContents(title,filters):
    for i in title:
        for j in filters:
            if i == j["world"]:
                return {
                    "status" : True,
                    "keyword" : j["world"]
                }
    return {
        "status" : False
    }

def IndividualVilter(title,filters):
    try:
        for i in filters:
            if title[i["index"]] == i["world"]:
                return False
        return True
    except BaseException as err:
        print(str(err))

def ValidatingSameData(data,text):
    for i in data:
        if i["title"] == text:
            return True
    return False

def CountTopik(topik,data):
    strings = ""
    for i in data:
        strings+=i
    splited = strings.split(" ")
    resultTopik = topik
    c = 0
    for i in topik:
        resultTopik[c]["count"] = 0
        for k in splited:
            if i["world"] == k.lower():
                resultTopik[c]["count"] += 1
        c +=1
    return resultTopik

@router.get("/hbase")
def hbase(request):
    connection = happybase.Connection(hbaseIp, int(hbasePort))
    table = connection.table('MDI')
    # connection.create_table('trycreateTable', { 'family': dict() } )
    # print(connection.tables())
    # table = []
    # for i in tables:
    #     table.append(i.decode("utf-8"))
    rows = table.scan(row_prefix=b'4ABZ')
    print(rows)
    datas = []
    for key, data in rows:
        # datas.append(data)
        i = {}
        for name,dict_ in data.items():
            print("==============================")
            i[name.decode("utf-8")] = json.loads(dict_.decode("utf-8"))
            print("==============================")
        datas.append(i)
        # a = data.values()
        # for i in a :
        #     b = i.decode('utf-8')
        #     datas.append(json.loads(b))
    connection.close()
    # print(datas)
    # jsoned = json.dumps(rows)
    # print(jsoned)
    return {
        "message" : "Success",
        "data" : datas
    }