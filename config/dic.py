#-*-coding:utf-8-*-
import re
import requests
import demjson
from plugin.msgutil import MsgUtil
from config.config import Config
from plugin.fileutil import FileUtil
import time

headers = Config.headers
csrf_token = Config.csrf_token
robotUid = Config.robot_uid
msgutil = MsgUtil(headers,csrf_token,robotUid)
fileutil = FileUtil()

#DIC词库内容
#updateAck新版本直接在消息获取时完成，以后可以不加入


#发送文本
def sendText(userMsg,robotUid,senderUid):


    if userMsg == "菜单":
        Msg = '来份萝莉\\n你好 聊天内容\\n御坂网络登录申请\\nBig图片降噪\\n原神模块'
        print(msgutil.sendMsg(Msg,robotUid,senderUid))
        
    #字符串匹配
    if userMsg == "你好":
        Msg = "你也好"
        #发送者UID 接受UID
        print(msgutil.sendMsg(Msg,robotUid,senderUid))

    

    if userMsg == "你是不是萝莉":
        Msg = '不不不，我想不是'
        print(msgutil.sendMsg(Msg,robotUid,senderUid))

    if userMsg =="来份萝莉":
        imageUrl = msgutil.upcoverImage("https://api.dongmanxingkong.com/suijitupian/acg/1080p/index.php")
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

    if re.search('^原神游戏公告 ?(.*?)$', userMsg):
        MsgRe = re.compile('^原神游戏公告 ?(.*?)$')
        MsgReArray = MsgRe.findall(userMsg)

        getMsg = requests.get("https://pan.misakaloli.com/api/mihuyou/?form=game&type=getData&id="+str(MsgReArray[0])).text
        gameJson = demjson.decode(getMsg)
        print(gameJson)
        ImageUrl = gameJson['imageurl'];
        activityUrl = gameJson['activityUrl']
        #直接上传文件文件

        #图片发送失败时用下载上传，代码如下
        imageUrl = msgutil.upcoverImage(ImageUrl)
        imageFormat = msgutil.getImageFormat(imageUrl)
        imageWidth = imageFormat[0]
        imageHeight = imageFormat[1]
        imageFormat = imageFormat[2]
        msgutil.sendImage(imageUrl,robotUid,senderUid,imageWidth,imageHeight,imageFormat)

        msgutil.sendMsg("详细信息如下\\n"+str(activityUrl),robotUid,senderUid)

    if re.search('^原神活动公告 ?(.*?)$', userMsg):
        MsgRe = re.compile('^原神活动公告 ?(.*?)$')
        MsgReArray = MsgRe.findall(userMsg)

        getMsg = requests.get("https://pan.misakaloli.com/api/mihuyou/?form=activity&type=getData&id="+str(MsgReArray[0])).text
        gameJson = demjson.decode(getMsg)
        ImageUrl = gameJson['imageurl'];
        activityUrl = gameJson['activityUrl']
        print(gameJson)

        imageUrl = msgutil.captureIamgeUrl(ImageUrl)
        imageFormat = msgutil.getImageFormat(imageUrl)
        imageWidth = imageFormat[0]
        imageHeight = imageFormat[1]
        imageFormat = imageFormat[2]
        msgutil.sendImage(imageUrl,robotUid,senderUid,imageWidth,imageHeight,imageFormat)

        msgutil.sendMsg("详细信息如下\\n"+str(activityUrl),robotUid,senderUid)


        

#发送图片
def sendImage(imageJson,receiverId,senderUid):
    imageUrl = imageJson['url']
    imageType = imageJson['imageType']
    imageHeight = imageJson['height']
    imageWidth = imageJson['width']

    Msg = '图片地址：' + imageUrl + '\\n图片格式：' + imageType
    print(msgutil.sendMsg(Msg,robotUid,senderUid))
    msgutil.updateAck(senderUid,csrf_token)
    # 这里我给个建议，先让用户发送指令，机器人把数据记录一下，然后判断如果下面有这个记录，做相应操作就可以

#发现撤回文本
def withdrawText(userMsg,robotUid,senderUid):
    Msg = '检测到你撤回了内容：' + userMsg
    print(msgutil.sendMsg(Msg,robotUid,senderUid))
    msgutil.updateAck(senderUid,csrf_token)
    
#发现撤回图片
def withdrawImage(imageJson,receiverId,senderUid):
    imageUrl = imageJson['url']
    imageType = imageJson['imageType']
    imageHeight = imageJson['height']
    imageWidth = imageJson['width']

    Msg = '检测到撤回了图片\\n图片地址：' + imageUrl + '\\n图片格式：' + imageType
    print(msgutil.sendMsg(Msg,robotUid,senderUid))
    msgutil.updateAck(senderUid,csrf_token)
    pass


'''
阅读信息 -> 目前一口气给B站上传，代表你已读信息 我并不清楚是否多余请求，请其他开发者指正
@Mid 读取私信用户UID
@csrf_token 鉴权值
 @return 返回信息
'''
def updateAck(Mid,ack_seqno,csrf_token):
    post_data = {'talker_id':Mid,'session_type':1,'ack_seqno':ack_seqno,'build':0,'mobi_app':"web","csrf_token":csrf_token,"csrf":csrf_token}
    fa =  requests.post('https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack',post_data,headers=headers)
    return fa.text

    


#直播文本发送
def liveSendText(userMsg,rommid):

    if userMsg == "测试":
        #发送直播消息
        msgutil.liveSendMsg("你好，我是御坂妹妹",rommid)


    #正则表达式区域
    re1 = re.search('^你好 ?(.*?)$', userMsg)
    if re1:
        MsgRe = re.compile('^你好 ?(.*?)$')
        MsgReArray = MsgRe.findall(userMsg)
        print(MsgReArray[0])
        getMsg = requests.get("http://i.itpk.cn/api.php?question="+str(MsgReArray[0])+"&api_key=45c0866382610cbee9bbbffaef5aa943&api_secret=ffnzr6hrzzaj&limit=8")
        getMsg.encoding = 'utf-8'
        getMsg = getMsg.text
        print(msgutil.liveSendMsg(getMsg,rommid))