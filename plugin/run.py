#-*-coding:utf-8-*-
#网络模块导入
import requests
#json模块导入
import demjson
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
SocketState = Config.SocketState
live_heartbeat_interval = Config.live_heartbeat_interval
live_id = Config.live_id
liveDicState = Config.liveDicState
msgutil = MsgUtil(headers,csrf_token,robotUid)


def run():
    # 启动一个线程，后台介绍信息，使得后续机器人可正常检测内容
    if SocketState:
        webHookThread = threading.Thread(target=robotSocket)
        # start启动线程
        webHookThread.start()
    #同上
    if liveDicState:
        liveThread = threading.Thread(target=liveBroadcastRun)
        liveThread.start()

    #给操作类必要参数，后面你可以自己补充
    while (True):
        time.sleep(heartbeatInterval)
        #获取时间戳
        thisTime = time.time()
        #精确改变
        thisTime = round(thisTime * 1000000)
        #心跳导致的延误时间计算
        pastTime = round(heartbeatInterval * 1000000)
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
                    #消息阅读
                    dic.updateAck(senderUid,ack_seqno,csrf_token)
                    webHookThread = threading.Thread(target=webHook,args=(newMsg,1))
                    # start启动线程
                    webHookThread.start()
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
$userMsg = json_decode(file_get_contents('php://input'), true);
file_put_contents('new.txt', $userMsg);
//用户信息
$Msg = $userMsg["data"]["session_list"][0]["last_msg"]["content"];
$Msg = json_decode($Msg, true);
$Msg = $Msg['content'];
//用户UID -> 受信UID
$senderUid = $userMsg['data']['session_list'][0]["last_msg"]['receiver_id'];
//机器人UID-> 发信UID
$receiverid = $userMsg['data']['session_list'][0]["last_msg"]['sender_uid'];
//消息类型 1是文本 2是图片
$msg_type = $userMsg['data']['session_list'][0]["last_msg"]["msg_type"]
$array = [
    'msg_type' => 1,
    'receiverid' =>$receiverid,
    'senderuid' => $senderUid,
    'msg' => $Msg
];
echo json_encode($array, JSON_UNESCAPED_UNICODE);

'''
def webHook(newJson,key):
    if webHookState:
        headers = {
        'Connection': 'close',
        'Content-Type': 'application/json;charset=UTF-8'
        }
        i = 0
        while i < len(webHookUrl):
            webHookMsgStr = requests.post(url=webHookUrl[i], data=demjson.encode(newJson),headers=headers)
            # 挂钩词库事件
            if webHookDicState:
                MsgJson = demjson.decode(webHookMsgStr.text)
                print(MsgJson)
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


#直播函数
def liveBroadcastRun():
    #创建一个储存发信时间的数组 -> 以免机器人重复测信
    msg_dictionary = []
    #创建数组计数值 当达到设定值后清理多余数据以免造成数组过长，运行迟钝
    max_count = 1000
    while True:
        #暂停一段时间
        time.sleep(live_heartbeat_interval)
        #请求接口开始轮询
        newMsgGet =  requests.get("https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid="+str(live_id),headers=headers)
        newMsgGet.encoding = 'utf-8'
        newMsg = demjson.decode(newMsgGet.text)
        #获取普通用户弹幕
        roomArrayJson = newMsg['data']['room']
        i = 0
        #轮询检测是否有重复
        while i < len(roomArrayJson):
            msgData = roomArrayJson[i]
            msgTime = msgData['check_info']['ct']
            Msg = msgData['text']
            uid = msgData['uid']
            #判断是否为机器人自己发送的内容
            if int(uid) != robotUid:
                #判断直播间是否有原来的信息 直播间数目 对比 记录时间条数 以此过滤原有内容
                if len(roomArrayJson) < len(msg_dictionary):
                    #判断这条信息是否已经被读取回复了 B站最多支持10条，也就是最多会重复刷新10次 每次3秒多一点
                    if msgTime in msg_dictionary:
                        #信息已经存在 不做操作 这里留个位置，我担心以后有用
                        pass
                    else:
                        #信息不存在则添加鸡记录信息
                        msg_dictionary.append(msgTime)
                        #推送消息
                        dic.liveSendText(Msg,live_id)
                        #判断数组是否达到峰值，如果达到则清空
                        if len(msg_dictionary) > max_count:
                            del msg_dictionary[0:max_count-10]
                            pass
                else:
                    #不存在则否则记录
                    msg_dictionary.append(msgTime)
            i = i + 1
            
    


