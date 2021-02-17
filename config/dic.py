#-*-coding:utf-8-*-
import re
import requests
from plugin.msgutil import MsgUtil
from config.config import Config

headers = Config.headers
csrf_token = Config.csrf_token
robotUid = Config.robot_uid
msgutil = MsgUtil(headers,csrf_token,robotUid)

#DIC词库内容
def sendText(userMsg,robotUid,senderUid):

    #字符串匹配
    if userMsg == "你好":
        Msg = "你也好"
        #发送者UID 接受UID
        print(msgutil.sendMsg(Msg,robotUid,senderUid))
        msgutil.updateAck(senderUid,csrf_token)

    if userMsg == "你是不是萝莉":
        Msg = '不不不，我想不是'
        print(msgutil.sendMsg(Msg,robotUid,senderUid))
        msgutil.updateAck(senderUid,csrf_token)

    if userMsg =="来份萝莉":
        imageUrl = msgutil.captureIamgeUrl("https://api.dongmanxingkong.com/suijitupian/acg/1080p/index.php")
        imageFormat = msgutil.getImageFormat(imageUrl)
        imageWidth = imageFormat[0]
        imageHeight = imageFormat[1]
        imageFormat = imageFormat[2]
        print(msgutil.sendImage(imageUrl,robotUid,senderUid,imageWidth,imageHeight,imageFormat))
        msgutil.updateAck(senderUid,csrf_token)

    #正则表达式区域
    re1 = re.search('^你好 ?(.*?)$', userMsg)
    if re1:
        MsgRe = re.compile('^你好 ?(.*?)$')
        MsgReArray = MsgRe.findall(userMsg)
        print(MsgReArray[0])
        getMsg = requests.get("http://i.itpk.cn/api.php?question="+str(MsgReArray[0])+"&api_key=45c0866382610cbee9bbbffaef5aa943&api_secret=ffnzr6hrzzaj&limit=8")
        getMsg.encoding = 'utf-8'
        getMsg = getMsg.text
        print(msgutil.sendMsg(getMsg,robotUid,senderUid))
        msgutil.updateAck(senderUid,csrf_token)
        pass


    pass

