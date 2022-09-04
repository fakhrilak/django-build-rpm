from ninja import Router
import tweepy
import json
from ninja import Schema
from time import gmtime, strftime
from portalTwitter.halperTwitter import TwitterPorTals
consumer_key = "m1IfyHbaKnpKfq1aUHnSpmWx5"
consumer_secret = "SLKNUIY9PJENSmcIG3YsIdtbvAZAweSvHI4KmeX8FSthQe9nBG"
access_token = "1431351007825444864-eFCWHsziG3jMQzTLbbCh4DfJE5QEMi"
access_token_secret = "38Ezfsxbkd0nqtF0akThVdaAyMZHSHSQW57dEX9pE9EF4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
router = Router()

class NewsScema(Schema):
    content:bool
    kafka: bool
    topicId: str
@router.get("/twitter/byareaname")
def TwitterAreaName(request,areaName:str):
    x = api.trends_available()
    for i in x:
        if(i["name"] == areaName.capitalize()):
            try:
                y = api.trends_place(i["woeid"])
                return {
                    "message" : "Success Get Tranding ",
                    "data" : y,
                    "status" : 200
                }
            except BaseException as err:
                return{
                    "message" : str(err),
                    "status" : 500
                }
    return {
        "message" : "area not found",
        "status" : 400
    }


@router.get("/twitter/tweet")
def getTwitterTwet(request,kafka:bool,topicId:str,length:int):
    print(kafka,topicId,length)
    try:
        twitter = TwitterPorTals(topicId)
        twitter.getConfig()
        twitter.doGetTwitte(length)
        if kafka == True:
            twitter.doSendKafka()
        # return {
        #     "data_dummy":twitter.dummy
        # }
        return{
            "message" : "success",
            "data" : twitter.data
        }
    except BaseException as err:
        return {
            "message" : str(err)
        }

class TwitterScema(Schema):
    length:int
    kafka: bool
    topicId: str
@router.post("/twitter/tweet")
def TwitterTwet(request,data:TwitterScema):
    try:
        twitter = TwitterPorTals(data.topicId)
        twitter.getConfig()
        twitter.doGetTwitte(data.length)
        if data.kafka == True:
            twitter.doSendKafka()
        # return {
        #     "data_dummy":twitter.dummy
        # }
        return{
            "message" : "success",
            "data" : twitter.data
        }
    except BaseException as err:
        return {
            "message" : str(err)
        }

@router.get("/twitter/usernameorid")
def TwitterGetByUserName(request,unic:str,types:str):
    try:
        if types == "id":
            data = api.get_user(id=int(unic))
        elif types == "username":
            data = api.get_user(unic)
        else:
            return {
                "message" : "Please insert type id or username"
            }
        return {
            "message" : "Success Get Data "+types+" "+ unic,
            "data" : data._json
        }
    except BaseException as err:
        return {
            "message" : str(err)
        }

# @router.get("/twitter/tweetid")
# def TwitterGetTweetId(request,tweetId:str):
#     try:
#         detailTweet = api.get_status(ids=tweetId)
#         print("masuk twwet id")
#         return {
#             "message":"Success get Tweet Id : "+id,
#             "data" : detailTweet._json
#         }
#     except BaseException as err:
#         return {
#             "message" : str(err)
#         }
