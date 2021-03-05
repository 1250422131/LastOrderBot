#-*-coding:utf-8-*-
#网络模块导入
import requests
#json模块导入
import demjson
import json
import time
import threading
from plugin.msgutil import MsgUtil
from config import dic
from config.config import Config
from socket import *


#获取全局配置
headers = Config.headers
csrf_token = Config.csrf_token
robotUid = Config.robot_uid
pythonDicState = Config.pythonDicState
heartbeatInterval = Config.heartbeat_interval
webHookState = Config.webHookState
webHookDicState = Config.webHookDicState
webHookUrl = Config.webHookUrl
msgutil = MsgUtil(headers,csrf_token,robotUid)


def run():
    # 启动一个线程，后台介绍信息，使得后续机器人可正常检测内容
    webHookThread = threading.Thread(target=robotSocket)
    # start启动线程
    webHookThread.start()
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
                #机器人ID
                receiverId = newMsgJson["last_msg"]["receiver_id"]
                #用户ID
                senderUid = newMsgJson["last_msg"]['sender_uid']
                #撤回消息与否 1是发送 0是撤回
                unread_count = newMsgJson["unread_count"]
                ack_seqno = int(newMsgJson["ack_seqno"]) + 1
                if robotUid == int(receiverId):
                    webHookThread = threading.Thread(target=webHook,args=(newMsgGet.text,1))
                    # start启动线程
                    webHookThread.start()
                    #消息阅读
                    dic.updateAck(senderUid,ack_seqno,csrf_token)
                    #dic 词库激活状态
                    if pythonDicState:
                        #消息类型 1是文本 2是图片
                        msg_type = newMsgJson["last_msg"]["msg_type"]
                        #消判信息
                        if unread_count >= 1 :
                            if msg_type == 1:
                                MsgJson = demjson.decode(newMsgJson["last_msg"]["content"])
                                Msg = MsgJson['content']
                                dic.sendText(Msg,receiverId,senderUid)
                            elif msg_type == 2 :
                                imageJson = demjson.decode(newMsgJson["last_msg"]["content"])
                                dic.sendImage(imageJson,receiverId,senderUid)
                        elif unread_count == 0:
                            if msg_type == 1:
                                MsgJson = demjson.decode(newMsgJson["last_msg"]["content"])
                                Msg = MsgJson['content']
                                dic.withdrawText(Msg,receiverId,senderUid)
                            elif msg_type == 2 :
                                print(newMsgJson["last_msg"]["content"])
                                imageJson = demjson.decode(newMsgJson["last_msg"]["content"])
                                dic.withdrawImage(imageJson,receiverId,senderUid)
                i = i + 1

        else:
            pass


'''
在这里我简单说一下配置webhook实际上是在给指定的网页主动发送一个JSON请求
下面我展示一下php的获取方式
其他网页语言百度一下
<?php
//接受传回来的JSON，并且进行解码
$update = json_decode(file_get_contents('php://input'), true);
//这里只是把获取到的内容储存下来，你用的话删掉，写你的词库逻辑代码，如果不需要，则可以忽略。
file_put_contents("./nex.txt",$update);
'''
def webHook(newJson,key):
    if webHookState:
        headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        "charset": "utf-8",
        'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
        }
        i = 0
        while i < len(webHookUrl):
            webHookMsgStr = requests.post(url=webHookUrl[i], data=demjson.encode(newJson),headers=headers)
            # 挂钩词库事件
            if webHookDicState:
                MsgJson = demjson.decode(webHookMsgStr.text)
                msg = MsgJson["msg"]
                # TODO 发送类型 1 是文本类型 Msg代表发送文本 2 是图片类型 Msg代表图片链接，，，，这必须是
                msg_type = MsgJson["msg_type"]
                # 收信UID
                receiverId = MsgJson["receiverid"]
                # 发信UID -> 一般为机器人UID
                senderUid = MsgJson["senderuid"]
                print(msg_type)
                if msg_type == 1:
                    print(msgutil.sendMsg(msg,senderUid,receiverId))
                elif msg_type == 2:
                    imageUrl = msgutil.captureIamgeUrl(msg)
                    imageFormat = msgutil.getImageFormat(imageUrl)
                    imageWidth = imageFormat[0]
                    imageHeight = imageFormat[1]
                    imageFormat = imageFormat[2]
                    msgutil.sendImage(imageUrl,senderUid,receiverId,imageWidth,imageHeight,imageFormat)
                pass
            i = i + 1

    #Socket 主要是用来作为外部通信的 假如你不会python语言，用其他的，就可以使用UDP通信

def robotSocket():
    print("==============RobotUDP服务端已经启动===================")
    host = '127.0.0.1' #主机号为空白表示可以使用任何可用的地址
    port = 2233 #端口号
    bufsiz = 1024 #接受数据缓冲大小
    addr = (host, port)
    udpSerSock = socket(AF_INET, SOCK_DGRAM)#创建udp服务器套接字
    udpSerSock.bind(addr) #套接字与地址绑定
    while True:
        print('等待接收消息...')
        data, addr = udpSerSock.recvfrom(bufsiz)#连续接受指定字节的数据，接收到的是字节数组
        MsgJson = demjson.decode(data)
        msg = MsgJson["msg"]
        # TODO 发送类型 1 是文本类型 Msg代表发送文本 2 是图片类型 Msg代表图片链接，，，，这必须是
        msg_type = MsgJson["msg_type"]
        # 收信UID
        receiverId = MsgJson["receiverid"]
        # 发信UID -> 一般为机器人UID
        senderUid = MsgJson["senderuid"]
        print(msg_type)
        if msg_type == 1:
            print(msgutil.sendMsg(msg,senderUid,receiverId))
        elif msg_type == 2:
            imageUrl = msgutil.captureIamgeUrl(msg)
            imageFormat = msgutil.getImageFormat(imageUrl)
            imageWidth = imageFormat[0]
            imageHeight = imageFormat[1]
            imageFormat = imageFormat[2]
            msgutil.sendImage(imageUrl,senderUid,receiverId,imageWidth,imageHeight,imageFormat)
        udpSerSock.sendto(bytes(data.decode('utf-8'), 'utf-8'), addr)#向客户端发送时间戳数据，必须发送字节数组
        print('响应消息到', addr)
    udpSerSock.close()#关闭服务器


