from ninja import Router
from aisportal.halperAis import KeyAccess
from aisportal.getAisData import getDataFromApiAis
import requests
import os
router = Router()

@router.get("/ais")
def getAisData(request):

    key = KeyAccess()
    mykey = key.myKeyAccess()

    ais = getDataFromApiAis(os.environ.get('aisDom'),mykey)
    data = ais.requestAIS()
    return { 
        "message" : "success",
        "data":data
    }
