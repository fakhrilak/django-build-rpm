from ninja import Router
import happybase
import json
from opensearchpy import OpenSearch
import os

kafkaIp=os.environ.get('kafkaIp')
openSearchIp=os.environ.get('openSearchIp')
openSearchPort=os.environ.get('openSearchPort')
hbaseIp=os.environ.get('hbaseIp')
hbasePort=os.environ.get('hbasePort')
apiPort=os.environ.get("apiPort")
apiIP=os.environ.get('apiIP')
client = OpenSearch("http://admin:admin@"+openSearchIp+":"+str(openSearchPort))

router = Router()

@router.get("/migrasi")
def migrasiElastics(request):
    try:
        query = {
                "size":100,
                "query": {
                    "match_all":{}
            }
        }
        response = client.search(
            body = query,
            index = "prajurit"
        )
        hist = response["hits"]["hits"]
        newdata = []
        for i in hist:
            newdata.append(i["_source"])
        count = 0
        for i in newdata:
            i["id"]=hist[count]["_id"]
            count +=1
        connection = happybase.Connection(hbaseIp,hbasePort,autoconnect=False)
        connection.open()
        table = connection.table('DEV')
        for i in newdata:
            for name,dict_ in i.items():
                # print(name)
                table.put(i["id"],{'1:'+str(name): json.dumps(i[str(name)])})
        connection.close()
        return {
            "message" : "Success",
            "len" : len(newdata),
            "data" : newdata
        }
    except BaseException as err:
        return {
            "message" : str(err)
        }