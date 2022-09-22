from ninja import Router
from aisportal.halperAis import KeyAccess
from aisportal.getAisData import getDataFromApiAis
import requests
import os

router = Router()

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
