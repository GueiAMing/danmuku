from mongofuction import dbmethod
import json
from datetime import datetime, timedelta, timezone
import threading

def getnowstate():
    mycol = dbmethod("wedding","test")
    mydoc = mycol.find_one({"_id":"1"},{"_id":0})
    state = mydoc["state"]
    return state

def getnickname_list():
    mycol = dbmethod("wedding","useridname")
    mydoc = mycol.find_one({"_id": "0"})
    nickname_list = mydoc["nickname"]
    return nickname_list

def getUseridList():
    mycol = dbmethod("wedding","useridname")
    mydoc = mycol.find_one({"_id":"0"},{"_id":0})
    userids = mydoc["userids"]
    return userids

def getBlackList():
    mycol = dbmethod("wedding","blacklist")
    mydoc = mycol.find_one({"_id":"0"},{"_id":0})
    userids = mydoc["userids"]
    return userids

def getUseridSentTime(userId):
    mycol = dbmethod("wedding","useridmessage")
    mydoc = mycol.find_one({"_id":userId})
    return mydoc

def getLastWroteTime(userId):
    mycol = dbmethod("wedding","useridmessage")    
    mydoc = mycol.find_one({"_id": userId})
    lasttime = mydoc["time"][-1]
    return lasttime

def getResendnicknameText():
    message = {
                "type":"text",
                "text":"因為該暱稱已存在，請輸入其他暱稱"
    }
    return message

def getRemoveblackmemberSucessfulText(nickname):
    message = {
                "type":"text",
                "text":f"{nickname}從黑名單移除成功"
    }
    return message

def getWirteinblacklistByhandText(nickname):
    message = {
                "type":"text",
                "text":f"{nickname}手動加入黑名單成功"
    }
    return message

def getTooLongMessageText():
    message = {
                "type":"text",
                "text":"請把留言控制在15個字以內"
    }
    return message

def getChangeModeNonmessageText():
    message = {
                "type":"text",
                "text":"切換為一般模式"
    }
    return message

def getRetrySendNicknameText():
    message = {
                "type":"text",
                "text":"請輸入別的暱稱"
    }
    return message

def getChangeModeText():
    message = {
                "type":"text",
                "text":"切換為留言模式"
    }
    return message

def getWriteMessageTime(userId,message):
    lock = threading.Lock()
    with lock:
        try:
            mycol = dbmethod("wedding","useridmessage")
            message_list = []
            message_list.append(message)
            datetime_list=[]
            datetime_list.append(datetime.now())
            mycol.update_one({"_id": userId},{"$set":{"message":message_list,"time":datetime_list}},True)
            print("資料寫入成功，IN TRY")
        except:
            mycol = dbmethod("wedding","useridmessage")
            message_list = []
            message_list.append(message)
            datetime_list=[]
            datetime_list.append(datetime.now())
            mycol.update_one({"_id": userId},{"$set":{"message":message_list,"time":datetime_list}},True)
            print("資料寫入成功，IN EXCEPT")

def getRemoveblackmember(nickname):
    lock = threading.Lock()
    with lock:
        try:
            mycol = dbmethod("wedding","blacklist")
            mydoc = mycol.find_one({"nickname": nickname})
            userid = mydoc["_id"]
            mydoc = mycol.find_one({"_id": "0"})
            userid_list = mydoc["userids"]
            userid_list.remove(userid)
            mycol.update_one({"_id": "0"},{"$set":{"userids":userid_list}},True)
            print("資料寫入成功，IN TRY")
        except:
            mycol = dbmethod("wedding","blacklist")
            mydoc = mycol.find_one({"nickname": nickname})
            userid = mydoc["_id"]
            mydoc = mycol.find_one({"_id": "0"})
            userid_list = mydoc["userids"]
            userid_list.remove(userid)
            mycol.update_one({"_id": "0"},{"$set":{"userids":userid_list}},True)
            print("資料寫入成功，IN EXCEPT")



def getWriteMessageTimeTwo(userId,message):
    lock = threading.Lock()
    with lock:
        try:
            mycol = dbmethod("wedding","useridmessage")
            mydoc = mycol.find_one({"_id":userId})
            message_list = mydoc["message"]
            message_list.append(message)
            datetime_list = mydoc["time"]
            datetime_list.append(datetime.now())
            mycol.update_one({"_id": userId},{"$set":{"message":message_list,"time":datetime_list}},True)
            print("資料寫入成功，IN TRY")
        except:
            mycol = dbmethod("wedding","useridmessage")
            mydoc = mycol.find_one({"_id":userId})
            message_list = mydoc["message"]
            message_list.append(message)
            datetime_list = mydoc["time"]
            datetime_list.append(datetime.now())
            mycol.update_one({"_id": userId},{"$set":{"message":message_list,"time":datetime_list}},True)
            print("資料寫入成功，IN EXCEPT")


def getConfirmNickname(nickname):
    data = json.dumps({'nickname':nickname, 'action':'confirm nickname'})
    message = {
                "type": "template",
                "altText": "this is a confirm template",
                "template": {
                    "type": "confirm",
                    "text": f"是否您的暱稱為\"{nickname}\"",
                    "actions": [
                    {
                        "type": "postback",
                        "label": "是",
                        "data": data,
                        "displayText": "是",
                    },
                    {
                        "type": "message",
                        "label": "否",
                        "text": "否"
                    }
                    ]

                }
            }
    
    

    return message

def getConfirmSendText(text, nickname):
    data = json.dumps({'message':text, 'nickname':nickname,'action':'sending Message'})
    message = {
                "type": "template",
                "altText": "this is a confirm template",
                "template": {
                    "type": "confirm",
                    "text": f"將傳送\"{text}\"至大螢幕上，是否傳送？",
                    "actions": [
                    {
                        "type": "postback",
                        "label": "是",
                        "data": data,
                        "displayText": "是",
                    },
                    {
                        "type": "message",
                        "label": "否",
                        "text": "否"
                    }
                    ]

                }
            }
    return message


def getUseridNickname():
    message = {
    "type": "flex",
    "altText": "this is a flex message",
    "contents": {
            "type": "bubble",
            "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "請點選下方按鈕提供您的暱稱，您可以稱呼自己\'政大金城武\'或者\'松山宋慧喬\'",
                            "wrap": True
                        }
                        ]
                    },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "點我",
                        "data": json.dumps({"action":"My nickname example"}),
                        "inputOption": "openKeyboard",
                        "fillInText":"我的暱稱："
                    }
                },
                
                ]
            }
            }
    }
    return message

def getReadyToSendMessageText(nickname):
    message = {
                "type":"text",
                "text":f"歡迎\'{nickname}\'，可以發送留言至大螢幕了"
                }
    

    return message

def getExampleMessageText():
    message = {
                "type":"text",
                "text":f"輸入\n\'留言：百年好合\'\n\'百年好合\'就會顯示在大螢幕上"
                }
    

    return message

def getSentYourMessageText(text):
    message = {
                "type":"text",
                "text":f"\"{text}\"已傳送"
             }
    

    return message

def getWaitOneminuteText():
    message = {
                "type":"text",
                "text":f"請於一分鐘後再傳送，謝謝"
             }
    

    return message

def getYouAreBlackmember():
    message = {
                "type":"text",
                "text":f"很抱歉，您輸入的內容可能有不雅字眼，所以您被加入黑名單了"
             }
    

    return message

