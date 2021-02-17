#-*-coding:utf-8-*-
#网络模块导入
import requests
#json模块导入
import demjson
import time
from bilibiliRobot.config import dic
from bilibiliRobot.config.config import Config

#获取全局配置
headers = Config.headers
csrf_token = Config.csrf_token
robotUid = Config.robot_uid
heartbeatInterval = Config.heartbeat_interval



def run():
    #给操作类必要参数，后面你可以自己补充
    while (True):
        time.sleep(heartbeatInterval)
        #获取时间戳
        thisTime = time.time()
        #精确改变
        thisTime = round(thisTime * 1000000)
        #心跳导致的延误时间计算
        pastTime = round(heartbeatInterval * 2000000)
        #获取正确时间戳
        thisTime = int(thisTime) - pastTime
        #请求信息接口
        newMsgGet =  requests.get("https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?begin_ts="+str(thisTime)+"&build=0&mobi_app=web",headers=headers)
        newMsgGet.encoding = 'utf-8'
        newMsg = demjson.decode(newMsgGet.text)
        #判断是否有新消息
        if "session_list" in str(newMsg):
            i = 0
            #拉取新消息条数
            while i < len(newMsg['data']['session_list']):
                newMsgJson = newMsg['data']['session_list'][i]
                receiverId = newMsgJson["last_msg"]["receiver_id"]
                senderUid = newMsgJson["last_msg"]['sender_uid']
                if robotUid == int(receiverId):
                    if "url" in str(newMsgJson["last_msg"]["content"]):
                        imageJson = demjson.decode(newMsgJson["last_msg"]["content"])
                        imageUrl = imageJson['url']
                        imageType = imageJson['imageType']
                    else:
                        MsgJson = demjson.decode(newMsgJson["last_msg"]["content"])
                        Msg = MsgJson['content']
                        dic.sendText(Msg,receiverId,senderUid)
                i = i + 1
        else:
            pass