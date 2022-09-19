import requests
import time
import json
class getDataFromApiAis():

    def __init__(self,domainAis,KeyAccess):
        print(KeyAccess, " =================== ",domainAis)
        self.domain = domainAis
        self.endPoint = str(domainAis+"home/sit/ops/ais/"+KeyAccess+"/")
    
    def requestAIS(self):
        try:
            print(self.endPoint,"inininiin")
            res = requests.request("GET",url = self.endPoint,
            headers={},data={},verify=False)
            time.sleep(5)
            # print(res.status_code,"ini")
            if(res.status_code == 200):
                jsoned = json.loads(res.text)
                return jsoned["data"]["results"]
            else:
                return json.loads([])
        except BaseException as err:
            print(str(err))
            return str(err)