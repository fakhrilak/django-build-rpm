from ninja import Router
import hashlib
from aisportal.halperAis import KeyAccess
from aisportal.getAisData import getDataFromApiAis
import happybase
import json
import requests
from six import ensure_binary
import json
import os

hbaseIp=os.environ.get('hbaseIp')
hbasePort=os.environ.get('hbasePort')
router = Router()
# connection = happybase.Connection(hbaseIp,int(hbasePort),transport='framed')
# connection = happybase.Connection(hbaseIp,int(hbasePort))
@router.get("/ais")
def getAisData(request,kafka:bool):

    key = KeyAccess()
    mykey = key.myKeyAccess()

    ais = getDataFromApiAis(os.environ.get('aisDom'),mykey)
    data = ais.requestAIS()
    if kafka == True & len(ais.data) > 0:
        ais.doSendKafka()
    return { 
        "message" : "success",
        "data":data
    }

@router.post("/ais/history/{mmishash}/{mmis}")
def addAisHistory(request,mmishash:str,mmis:str):
    print("req masuk")
    # connection = happybase.Connection(hbaseIp,int(hbasePort))
    connection = happybase.Connection(hbaseIp,int(hbasePort),transport='framed')
    connection.open()
    table = connection.table('AIS_HISTORY')
    row = table.row(mmis.encode('utf-8'))
    if row:
        print("====================== APPEND HISTORY =========================")
        print(row)
        for name,dict_ in row.items():
            for i in json.loads(dict_.decode("utf-8")):
                if i == mmishash:
                    print(i)
                    connection.close()
                    return {
                        "message" : "data sudah ada",
                        "status" : 400
                    }
            ############## add new arry history
            historyAIS = json.loads(dict_.decode("utf-8"))
            historyAIS.append(mmishash)
            jsoned = json.dumps(historyAIS)
            table.put(mmis, {'AIS_VASSEL_POSITIONS:data':jsoned})
            connection.close()
    else:
        print("====================== CREATE RAW =============================")
        jsoned = json.dumps([mmishash])
        table.put(mmis, {'AIS_VASSEL_POSITIONS:data':jsoned})
    # print(row)
    connection.close()
    # decodes = hashlib.md5(mmishash.encode('utf-8')).hexdigest()
    # print(hashlib.md5(decodes.encode('utf-8')).hexdigest())
    return {
        "message" : "success",
        "data"  : mmishash,
        "data1" : mmis
    }
@router.get("/coba/{mmis}")
def getData(request,mmis:str,page:str,size:str):
    try:
        # connection = happybase.Connection(hbaseIp,int(hbasePort))
        connection = happybase.Connection(hbaseIp,int(hbasePort),transport='framed')
        connection.open()
        table = connection.table('AIS_HISTORY')
        row = table.row(mmis.encode('utf-8'))
        newsdata = ""

        if row:
            print("ada")
            for name,dict_ in row.items():
                newsdata = json.loads(dict_.decode("utf-8"))
            resultdata = []
            table = connection.table('AIS_VASSEL_POSITIONS')
            if len(newsdata) < int(size):
                connection.close()
                return {
                    "message" : "size > jumlah data",
                    "status" : 400
                }
            newsdata = [newsdata[i:i+int(size)] for i in range(0, len(newsdata), int(size))]
            print(newsdata,"ini")
            #################################### GET HISTORY
            for i in newsdata[0]:
                print(i)
                rows = table.row(i.encode('utf-8'))
                datas = {}
                for key,data in rows.items():
                    # print(data)
                    key = key.decode("utf-8")
                    datas[key[21:len(key)]] = data.decode("utf-8")
                datas["type"] = "Feature"
                datas["is_anom"] = False
                datas["geometry"] = {
                             "type": "Point",
                             "coordinates": [
                                    float(datas["longitude"]),
                                    float(datas["latitude"])
                            ]
                        }
                resultdata.append(datas)
            connection.close()
            return {
                "data": {
                    "data": resultdata[int(page)-1],
                    "totalItems": int(size),
                    "totalPage": len(newsdata),
                    "currenPage" : int(page)
                },
                "desc": "Ok",
                "message": "Search Succeed",
                "status": 200
            }
            
        else:
            connection.close()
            return {
                "message" : "tidak ada data dengan mmis",
                "status" : 400
            }
    except BaseException as err:
        connection.close()
        return {
            "message" : str(err)
        }

@router.get("/ais/{mmis}")
def getDataBymmis(request,mmis:str,page:str,size:str):
    try:
        # connection = happybase.Connection(hbaseIp,int(hbasePort))
        # connection.open()
        # table = connection.table('AIS_VASSEL_POSITIONS')
        # datas= []
        # try:
        #     for key, data in table.scan():
        #         # print("masuk sini")
        #         newdata = {}
        #         for name,dict_ in data.items():
        #             name = name.decode("utf-8")
        #             dict_= dict_.decode("utf-8")
        #             print(dict_,mmis)
        #             if dict_ == str(mmis):
        #                 # datas.append(dict_.decode("utf-8"))
        #                 for name2,dict_2 in data.items():
        #                     name2 = name2.decode("utf-8")
        #                     dict_2= dict_2.decode("utf-8")
        #                     print(dict_2)
        #                     newdata[name2[21:len(name2)]] = dict_2
        #                 newdata["geometry"] = {
        #                      "type": "Point",
        #                      "coordinates": [
        #                             float(newdata["longitude"]),
        #                             float(newdata["latitude"])
        #                     ]
        #                 }
        #                 datas.append(newdata)
        # except:
        #     pass
        # # ais_id = hashlib.md5(mmis.encode('utf-8')).hexdigest()
        # # table = connection.table('AIS_SHIPINFO')
        # # byte = ais_id.encode('utf-8')
        # # row = table.row(byte)
        # # info = {}
        # # for name,dict_ in row.items():
        # #     name = name.decode("utf-8")
        # #     dict_ = dict_.decode("utf-8")
        # #     info[name[13:len(name)]] = dict_
        # connection.close()
        # if(len(datas) == 0):
        #     return {
        #         "message" : "data not found",
        #         "status" :  404
        #     }
        
        # pages = [datas[i:i+1] for i in range(0, len(datas), 1)]
        # return {
        #     "data" : {
        #         "data": datas[0],
        #         "totalItems": len(pages),
        #         "totalPage" :1
        #     },
        #      "desc": "Ok",
        #     "message": "Search Succeed",
        #     "status": 200
        # }
        test=[]
        for i in range(20):
            print(i)
            test.append({
                "count": i,
                "beam": "None",
                "cog": "0.0",
                "course": "0",
                "date_time": "2022-03-25",
                "destination": " ",
                "eta": " ",
                "heading": "511",
                "imo": "0",
                "kafka.offset": "69711",
                "kafka.partition": "0",
                "kafka.timestamp": "1664642122290",
                "kafka.topic": "AISCollect",
                "latitude": "1.2226",
                "location": "None",
                "longitude": "103.73068",
                "mmsi": "5638280",
                "nav_status": "Unknown",
                "nav_status_code": "0",
                "rot": "0",
                "sog": "0.0",
                "source": "T-AIS",
                "source_type": "SPIRE",
                "type" : "Feature",
                "speed": "0",
                "timestamp": "",
                "updated_time": "2022-03-25 17:31:49.051",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                    103.73068,
                    1.2226
                    ]
                }
                })
        pages = [test[i:i+int(size)] for i in range(0, len(test), int(size))]
        print(pages,"ini page")
        return {
            "data": {
                "data": pages[int(page)-1],
                "totalItems": len(test),
                "totalPage": len(pages),
                "currentPage": int(page)
            },
            "desc": "Ok",
            "message": "Search Succeed",
            "status": 200
            }
    except BaseException as err:
        if(str(err) == "list index out of range"):
            pages = [test[i:i+int(2)] for i in range(0, len(test), int(2))]
            print(pages,"ini page")
            return {
                "data": {
                    "data": pages[int(1)-1],
                    "totalItems": len(test),
                    "totalPage": len(pages),
                    "currentPage": int(page)
                },
                "desc": "Ok",
                "message": "please check page and size",
                "status": 200
                }
        return {
            "message" : str(err),
            "status"  : 500
        }