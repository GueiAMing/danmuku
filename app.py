from __future__ import unicode_literals
import eventlet
eventlet.monkey_patch()
from flask import Flask, request, abort, render_template
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from mongofuction import dbmethod
from bad_word_function import getbadword
from functions import getWirteinblacklistByhandText, getRemoveblackmemberSucessfulText, getRemoveblackmember, getTooLongMessageText, getResendnicknameText, getnickname_list, getRetrySendNicknameText, getChangeModeNonmessageText, getYouAreBlackmember, getBlackList, getnowstate, getChangeModeText, getUseridList, getConfirmNickname, getUseridNickname, getReadyToSendMessageText, getExampleMessageText, getConfirmSendText, getSentYourMessageText, getUseridSentTime, getLastWroteTime, getWaitOneminuteText,getWriteMessageTime,getWriteMessageTimeTwo
from datetime import datetime, timedelta, timezone
import threading
import csv
import os
import pymongo
import requests
import json
import configparser
from flask_socketio import SocketIO
import time


app = Flask(__name__, static_url_path='/static')

config = configparser.ConfigParser()
config.read('config.ini')

configuration = Configuration(access_token=config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}

socketio = SocketIO(app, async_mode='eventlet')
socketio.init_app(app, cors_allowed_origins='*')

USERIDSLIST= None
BLACKUSERIDSLIST= None
USERIDSLIST = set(getUseridList())
print(USERIDSLIST)
BLACKUSERIDSLIST =set(getBlackList())
print("黑",BLACKUSERIDSLIST)
BAD_WORDS = getbadword()
@app.route('/')
def index():
    return render_template('dan.html')

@app.route("/callback", methods=['POST', 'GET'])
def linebot():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    if request.method == 'POST' and len(events) == 0:
        return 'ok'
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        userId = events[0]["source"]["userId"]
        state = getnowstate()
        if state == 0 :
            if events[0]["type"] == "message":
                if events[0]["message"]["type"] == "text":
                    text = events[0]["message"]["text"]
                    if "我的暱稱：" in text:
                        nickname = text[5:]
                        count1 = 0
                        for word in BAD_WORDS:
                            if word in nickname:
                                count1 +=1
                                print(count1,word)
                        if count1 > 1:
                            print("不雅文字")
                            payload["messages"] = [getRetrySendNicknameText()]
                        else:
                            nickname_list = getnickname_list()
                            if nickname in nickname_list:
                                payload["messages"] = [getResendnicknameText()]
                            else:    
                                payload["messages"] = [getConfirmNickname(nickname)]
                    if text == "我要留言":
                        if userId not in USERIDSLIST:
                            
                            payload["messages"] = [getUseridNickname()] 
                            message = text
                    if userId not in BLACKUSERIDSLIST and "留言：" in text:
                        message = text[3:]
                        count = 0
                        if len(message) > 15:
                            payload["messages"] = [getTooLongMessageText()]
                        else:
                            for word in BAD_WORDS:
                                if word in message:
                                    count +=1
                                    print(count,word)
                            if count == 1:
                                mycol = dbmethod("wedding","useridname")
                                mydoc = mycol.find_one({'_id': userId})
                                nickname = mydoc['nickname']
                                message = nickname +"說："+ message
                                text = message
                                payload["messages"] = [getConfirmSendText(text,nickname)]
                            else:
                                mycol = dbmethod("wedding","useridname")
                                mydoc = mycol.find_one({'_id': userId})
                                nickname = mydoc['nickname']
                                getWirteinblacklist(userId, nickname)
                                payload["messages"] = [getYouAreBlackmember()]
                    if text =="切換" and userId =="Udbef88085842fe25519b2fb3713b8f0a": 
                        mycol = dbmethod("wedding", "test")
                        mycol.update_one({"_id":"1"},{"$set":{"state":1}})
                        payload["messages"] = [getChangeModeNonmessageText()]
                    if "移除" in text and userId =="Udbef88085842fe25519b2fb3713b8f0a": 
                        nickname = text[2:]
                        getRemoveblackmember(nickname)
                        payload["messages"] = [getRemoveblackmemberSucessfulText(nickname)]
                    if "黑單" in text and userId =="Udbef88085842fe25519b2fb3713b8f0a": 
                        nickname = text[2:]
                        getWirteinblacklistByhand(nickname)
                        payload["messages"] = [getWirteinblacklistByhandText(nickname)]

        if state == 1 :
            text = events[0]["message"]["text"]         
            if text =="切換" and userId =="Udbef88085842fe25519b2fb3713b8f0a":
                mycol = dbmethod("wedding", "test")
                mycol.update_one({"_id":"1"},{"$set":{"state":0}})
                payload["messages"] = [getChangeModeText()]
        if events[0]["type"] == "postback":
            data = json.loads(events[0]["postback"]["data"])
            action = data["action"]
            if action == 'confirm nickname':
                nickname = data["nickname"]     
                getConfirmednickname(userId, nickname)
                payload["messages"] = [getReadyToSendMessageText(nickname),getExampleMessageText()]
            if action == 'sending Message':
                message = data["message"]
                nickname = data["nickname"] 
                if getUseridSentTime(userId) == None:
                    handle_message(message)
                    getWriteMessageTime(userId,message)
                    text = message
                    payload["messages"] = [getSentYourMessageText(text)]
                else:
                    lasttime = getLastWroteTime(userId)
                    diff = datetime.now() - lasttime
                    if diff.total_seconds() < 60:
                        payload["messages"] = [getWaitOneminuteText()]
                    else:
                        handle_message(message)
                        getWriteMessageTimeTwo(userId,message)
                        text = message
                        payload["messages"] = [getSentYourMessageText(text)]  
    
        replyMessage(payload)
   

    return "ok"

@app.route('/sendmessage', methods=['POST', 'GET'])
def send_message():
    if request.method == 'GET':
        return render_template('sendmessage.html', welcome_message=None)
    else:
        message = request.form.get('name')
        message_be_sent = f"{message},已傳送!"
        handle_message(message)
        return render_template('sendmessage.html', message_be_sent=message_be_sent)
    
@socketio.on('chat_message')
def handle_message(message):
    # 当收到来自客户端的消息时，将其广播为弹幕
    socketio.emit('danmaku', message)

'''利用Line api 中 reply分類作為機器人回覆功能的主要函式'''
def replyMessage(payload):
    url='https://api.line.me/v2/bot/message/reply'
    response = requests.post(url,headers=HEADER,json=payload)
    print(response.status_code)
    print(response.text)
    return 'OK'

def background_task():
    """Example of how to send server generated events to clients."""
    
    while True:
        
        with open("static/messages.txt", "r",encoding="utf-8") as f:
            for line in f.readlines():
                time.sleep(3)
                message = line
                print(f"sendbysystem:{line}")
                socketio.emit('danmakubackground', message)
                time.sleep(3)


def fetch_data_from_mongo():
    global USERIDSLIST
    global BLACKUSERIDSLIST
    while True:
        USERIDSLIST = set(getUseridList())
        print("資料更新:",USERIDSLIST)
        BLACKUSERIDSLIST =set(getBlackList())
        print("資料更新:黑",BLACKUSERIDSLIST)  # 根據需要進行調整
        time.sleep(10)  # 每10秒更新一次


def getConfirmednickname(userId, nickname):
        USERIDSLIST.add(userId)
        print(USERIDSLIST)
        lock = threading.Lock()
        tzone = timezone(timedelta(hours=8))
        nowyeardatetime = datetime.now(tz=tzone)
        nowyeardatetime = nowyeardatetime.isoformat()[:16].replace("T","-")
        with lock:
            try:
                mycol = dbmethod("wedding","useridname")
                mycol.update_one({"_id": "0"},{"$set":{"userids":list(USERIDSLIST)}})
                mycol.insert_one({"_id":userId,"nickname":nickname,"time":nowyeardatetime,"points":1})

                mydoc = mycol.find_one({"_id": "0"})
                nickname_list = mydoc["nickname"]
                nickname_list.append(nickname)
                mycol.update_one({"_id": "0"},{"$set":{"nickname":nickname_list}})

                print(f"{userId}獲得點數卡")
            except:
                print(f"{userId}獲得點數卡，失敗")

def getWirteinblacklist(userId, nickname):
        BLACKUSERIDSLIST.add(userId)
        print(BLACKUSERIDSLIST)
        lock = threading.Lock()
        tzone = timezone(timedelta(hours=8))
        nowyeardatetime = datetime.now(tz=tzone)
        nowyeardatetime = nowyeardatetime.isoformat()[:16].replace("T","-")
        with lock:
            try:
                mycol = dbmethod("wedding","blacklist")
                mycol.update_one({"_id": "0"},{"$set":{"userids":list(BLACKUSERIDSLIST)}})
                mycol.update_one({"_id": userId},{"$set":{"nickname":nickname,"time":nowyeardatetime}},True)
                print(f"{userId}加入黑名單")
            except:
                print(f"{userId}加入黑名單，失敗")

def getWirteinblacklistByhand(nickname):
    lock = threading.Lock()
    tzone = timezone(timedelta(hours=8))
    nowyeardatetime = datetime.now(tz=tzone)
    nowyeardatetime = nowyeardatetime.isoformat()[:16].replace("T","-")
    with lock:
        try:
            mycol = dbmethod("wedding","useridname")
            mydoc = mycol.find({"nickname": nickname})
            temp  = []
            for data in mydoc:
                temp.append(data)
                print(temp)
            userid = temp[-1]["_id"]

            mycol = dbmethod("wedding","blacklist")
            mydoc = mycol.find_one({"_id": "0"})
            userid_list = mydoc["userids"]
            userid_list.append(userid)
            mycol.update_one({"_id": "0"},{"$set":{"userids":userid_list}})
            mycol.update_one({"_id": userid},{"$set":{"nickname":nickname,"time":nowyeardatetime}},True)
            print("資料寫入成功，IN TRY")
        except:
            print("資料寫入成功，IN EXCEPT")

if __name__ == '__main__':
    # 啟動背景執行緒
    threading.Thread(target=fetch_data_from_mongo, daemon=True).start()
    socketio.start_background_task(target=background_task)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
