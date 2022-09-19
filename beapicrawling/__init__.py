import argparse
import os
import sys
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("start",type=str,help="starting django")
    parser.add_argument("-port",type=str,help="server crawling port default 8000")
    parser.add_argument("-kIp",type=str,help="192.x.x.x:port in string value (kafka ip)")
    parser.add_argument("-oIp",type=str,help="192.x.x.x in string value (opensearch ip)")
    parser.add_argument("-oPort",type=str,help="in ineteger value (opensearch port)")
    parser.add_argument("-hIp",type=str,help="192.x.x.x in string value (hbase ip)")
    parser.add_argument("-hPort",type=str,help="in integer value (hbase port)")
    parser.add_argument("-cIp",type=str,help="in string value (config api ip)")
    parser.add_argument("-cPort",type=str,help="in string value (config api port)")
    parser.add_argument("-aisDom",type=str,help="in string value")
    return parser.parse_args()

def environments(params):
    
    ################### SERPORT ENVIRONMENT ###################
    if(params.port != None):os.environ["port"]=str(params.port)
    else:os.environ["port"]=str(5900)
    ###########################################################

    ########################## KAFKA IP #######################
    if(params.kIp != None):os.environ["kafkaIp"]=str(params.kIp)
    else:os.environ["kafkaIp"]="192.168.10.1:2000"
    ###########################################################

    ####################### OPENSEARCH IP #####################
    if(params.oIp != None):os.environ["openSearchIp"]=str(params.oIp)
    else:os.environ["openSearchIp"]="192.168.10.1"
    ###########################################################

    ########################## OPENSEARCH PORT #######################
    if(params.oPort != None):os.environ["openSearchPort"]=str(params.oPort)
    else:os.environ["openSearchPort"]=str(3004)
    ##################################################################

    ######################### HBASE IP ########################
    if(params.hIp != None):os.environ["hbaseIp"]=str(params.hIp)
    else:os.environ["hbaseIp"]=str("192.168.10.1")
    ###########################################################

    ######################### HBASE PORT ########################
    if(params.hPort != None):os.environ["hbasePort"]=str(params.hPort)
    else:os.environ["hbasePort"]=str(6060)
    ###########################################################

    ######################### CONFIG IP ########################
    if(params.cIp != None):os.environ["apiIp"]=str(params.cIp)
    else:os.environ["apiIp"]=str("192.168.10.38")
    ###########################################################

    ######################### CONFIG PORT ########################
    if(params.cPort != None):os.environ["apiPort"]=str(params.cPort)
    else:os.environ["apiPort"]=str(2001)
    ########################################################### 

    ######################### CONFIG PORT ########################
    if(params.aisDom != None):os.environ["aisDom"]=str(params.aisDom)
    else:os.environ["aisDom"]=str("https://api.tnial.mil.id/")
    ########################################################### 
def main():
    try:
        path  = __file__
        splited = path.split("/")
        path=""
        for i in splited[1:-1]:
            path += "/"+i
        args = parse_args()
        if args.start == "start":
            environments(args)

            port =  os.environ.get('port')

            ##########################################################################################################################################
            print(" ========= Main ",os.environ.get('port'),os.environ.get('kafkaIp'),os.environ.get('openSearchIp'),os.environ.get('openSearchPort'),
            os.environ.get('hbaseIp'),os.environ.get('hbasePort'),os.environ.get('apiIp'),os.environ.get('apiPort')
            )
            ##########################################################################################################################################
            jsonenv = {
                "port" : port
            }

            jsonString = json.dumps(jsonenv,indent=4,sort_keys=True)
            jsonFile = open(path+"/data.json", "w")
            jsonFile.write(jsonString)
            jsonFile.close()

            os.system("python3 "+path+"/manage.py runserver 0:"+port)
        elif args.start == "stop":
            data = open((path+"/data.json"))
            data = json.load(data)
            port = data["port"]
            os.system("kill -9 $(lsof -t -i:"+str(port)+")")
    except BaseException as err:
        print(str(err))