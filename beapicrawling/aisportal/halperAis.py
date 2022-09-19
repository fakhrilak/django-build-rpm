import datetime
import hashlib
import json
import requests
from pytz import timezone
from os import environ


class KeyAccess():
    
    def __init__(self):
        pass
    
    def Sha512Hash(self,Password):
        HashedPassword = hashlib.sha512(Password.encode('utf-8')).hexdigest()
        return (HashedPassword)

    def myKeyAccess(self):
        dateNow = datetime.datetime.now(timezone('Asia/Jakarta'))
        pswd = str('4p1#s!T#'+dateNow.strftime('%a') +
                    '#'+dateNow.strftime('%b')+'#')
        today = str(str(dateNow).split(':')[0]).replace(' ', '-')
        return self.Sha512Hash(pswd+today)
