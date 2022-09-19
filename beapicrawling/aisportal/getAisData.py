import requests
import time
class getDataFromApiAis():

    def __init__(self,domainAis,KeyAccess):
        print(KeyAccess, " =================== ",domainAis)
        self.domain = domainAis
        self.endPoint = str(domainAis+"home/sit/ops/ais/"+KeyAccess+"/")
    
    def requestAIS(self):
        try:
            res = requests.request("GET",url = "http://api.tnial.mil.id/home/sit/ops/ais/675cc2ce24cecd94f8241f98a1b2e3e5fec9e99ba4f97f8106a42cf67da3ddc18848c0402b29b8f0fd3915bcd38837a8a0958f4be39a9f25dbbf9e4337f83ba8/",
            headers={},data={},verify=False)
            print(res.text," ========== ini")
            # print(res.status_code,"ini")
            return res.text
        except BaseException as err:
            print(str(err))
            return str(err)