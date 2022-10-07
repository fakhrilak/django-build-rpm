import requests
import time
import json
import os
import hashlib
from kafka import KafkaProducer
import os
import datetime

kafkaIp=os.environ.get('kafkaIp')
openSearchIp=os.environ.get('openSearchIp')
openSearchPort=os.environ.get("openSearchPort")
hbaseIp=os.environ.get('hbaseIp')
hbasePort=os.environ.get('hbasePort')
apiPort=os.environ.get("apiPort")
apiIP=os.environ.get('apiIp')

class getDataFromApiAis():

    def __init__(self,domainAis,KeyAccess):
        self.domain = domainAis
        self.endPoint = str(domainAis+"home/sit/ops/ais/"+KeyAccess+"/")
        self.data = []

    def requestAIS(self):
        try:
            res = requests.request("GET",url = self.endPoint,
            headers={},data={},verify=False)
            time.sleep(5)
            # print(res.status_code,"ini")
            if(res.status_code == 200):
                data = json.loads(res.text)
                seen = set()
                new_l = []
                
                ########################################### FILTER DOUBLE DATA
                for d in data["data"]["results"]:
                    t = tuple(d.items())
                    if t not in seen:
                        seen.add(t)
                        new_l.append(d)

                self.data = new_l
                ###############################################################
                # print(len(data["data"]["results"]),"sebelum filter")
                # print(len(self.data),"sesudah filter")
                return self.data[1]
            else:
                return json.loads([])
        except BaseException as err:
            print(str(err))
            return str(err)

    def convertDateTime(self,data):
        try:
            splited =  data.split(" ")
            # day = splited[1]
            # mouth = splited[2]
            # year = splited[3]
            # month_name = splited[2]
            # month_num = datetime.datetime.strptime(month_name, '%b').month
            # if len(str(month_num)) == 1:
            #     month_num = "0"+str(month_num)
            # else:
            #     month_num = str(month_num)
            # return (year+"-"+str(month_num)+"-"+day)
            return splited[0]
        except BaseException as err:
            return "-"

    def doSendKafka(self):
        try:
            producer = KafkaProducer(bootstrap_servers=[kafkaIp],
            # value_serializer=lambda m: json.dumps(m).encode('ascii')
            )
            count = 0
            for i in self.data:
                print(" ========= Sending to Kafka ",count)
                i["ais_id"] = hashlib.md5(i["mmsi"].encode('utf-8')).hexdigest()
                i["ais_pos_id"]=hashlib.md5((i["mmsi"]+"_"+i["date_time"]).encode('utf-8')).hexdigest()
                i["date_time"] = self.convertDateTime(i["date_time"])
                # i["map_location"] = {
                #     "lon" : str(i["longitude"]),
                #     "lat" : str(i["latitude"])
                # }
                # i["geometry"]= {
                #     "type": "Point",
                #             "coordinates": [
                #                 str(i["longitude"]),
                #                 str(i["latitude"])
                #         ]
                # }
                print(" ======================== " ,i , " ======================== SEBELUM PRODUCE")
                producer.send('AISCollect',  json.dumps(i).encode('utf-8'))
                count +=1
                time.sleep(0.1)
            payload = json.dumps({"id_setting": 5})
            headers = {"Content-Type":"application/json",
            "Authorization": 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI5ZXVnbnItZER1djF0WEVpMzBjbUVtRUJuTjhva0lRc0NmTWFWa3dxSEFRIn0.eyJleHAiOjE2NjU1NjgyMTAsImlhdCI6MTY2Mjk3NjIxMCwianRpIjoiZTQ2NWM4ZGItMGIyZi00MmM5LWJjNTMtMjgwOGI3OGZiOWVjIiwiaXNzIjoiaHR0cHM6Ly8xOTIuMTY4LjEwLjE4Ojg0NDMvYXV0aC9yZWFsbXMvT3BlblNlYXJjaFRlc3RLZXljbG9hayIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI3NDA3ZDFmNS0wMTllLTRlNjAtYmQ4My1mMDc0ODczZjE5ZWMiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJTU08tQUwiLCJzZXNzaW9uX3N0YXRlIjoiZTQ1NWVhNzUtMmUxZi00MzUzLWEwYWUtNTJkOWE0MDJjYmFjIiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW9wZW5zZWFyY2h0ZXN0a2V5Y2xvYWsiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiYXBwLXVzZXIiXX0sInJlc291cmNlX2FjY2VzcyI6eyJTU08tQUwiOnsicm9sZXMiOlsiVXNlciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJhZGRyZXNzIG9mZmxpbmVfYWNjZXNzIG1pY3JvcHJvZmlsZS1qd3QgcGhvbmUgZW1haWwgcHJvZmlsZSIsInNpZCI6ImU0NTVlYTc1LTJlMWYtNDM1My1hMGFlLTUyZDlhNDAyY2JhYyIsInVwbiI6InN5YXJpZiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiYWRkcmVzcyI6e30sIm5hbWUiOiJTeWFyaWYgSGlkYXlhdCIsImdyb3VwcyI6WyJkZWZhdWx0LXJvbGVzLW9wZW5zZWFyY2h0ZXN0a2V5Y2xvYWsiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiYXBwLXVzZXIiXSwicHJlZmVycmVkX3VzZXJuYW1lIjoic3lhcmlmIiwiZ2l2ZW5fbmFtZSI6IlN5YXJpZiIsImZhbWlseV9uYW1lIjoiSGlkYXlhdCIsImVtYWlsIjoic3lhcmlmaGlkYXlhdDQwMEBnbWFpbC5jb20ifQ.FDnLlC5G2CQ7PVyBlFtImUt90aNR4Ooi7CrUHcd3-1H94gp_BnH7NWW1dCSBZkvh4R_vnPl3VsH-ByIeHsv-cBRb8hzW_p0L25qfbIQJJigq4-b3Wi5r5QuBZ7nXRkiXgZufy4QIEQTq9Dr_MtEkrXzbhl0BZzH-HVY0jk-aQhyDwik_YtaYf0AlJmjpwQffzJz9KNKGkF1Ct5Iy7Gmo5pnj2WkwpI7Qq5AV41PdxGAUSe7JpZijsetHAIfE1y3RKmVcsWxj0xcvpLE0nt6luYqiQUW-ukaCivo9wzjo26SgGp0xPhvHyeqE0PdtzNP8K-3URFV4EBD0m6ak_meh0A' }
            response = requests.request("POST", url="http://"+apiIP+":"+apiPort+"/api/v1/log-setting", headers=headers, data=payload)
            print("====================================== " ,response.text)
            producer.close()
        except BaseException as err:
            return str(err)
