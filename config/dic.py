#-*-coding:utf-8-*-
import re
import requests
from plugin.msgutil import MsgUtil
from config.config import Config
from plugin.fileutil import FileUtil

headers = Config.headers
csrf_token = Config.csrf_token
robotUid = Config.robot_uid
msgutil = MsgUtil(headers,csrf_token,robotUid)
fileutil = FileUtil()

#DIC词库内容
#updateAck新版本直接在消息获取时完成，以后可以不加入
#此次更新新增多个检测项目
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


    re2 = re.search('^写入 .*? .*? .*?$', userMsg)
    if re2:
        MsgRe = re.compile('^写入 (.*?) (.*?) (.*?)$')
        MsgReArray = MsgRe.match(userMsg)
        fileutil.write(MsgReArray.group(1),MsgReArray.group(2),MsgReArray.group(3))
        print(msgutil.sendMsg("写入成功",robotUid,senderUid))
        msgutil.updateAck(senderUid,csrf_token)


    re3 = re.search('^读出 .*? .*?$', userMsg)
    if re3:
        MsgRe = re.compile('^读出 (.*?) (.*?)$')
        MsgReArray = MsgRe.match(userMsg)
        Msg = fileutil.read(MsgReArray.group(1),MsgReArray.group(2))
        print(msgutil.sendMsg(Msg,robotUid,senderUid))
        msgutil.updateAck(senderUid,csrf_token)
    pass

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
    requests.get("https://api.vc.bilibili.com/link_setting/v1/link_setting/is_limit?uid="+str(Mid)+"&type=1",headers=headers)
    requests.get("https://api.vc.bilibili.com/link_setting/v1/link_setting/get_session_ss?talker_uid="+str(Mid)+"&build=0&mobi_app=web",headers=headers)
    requests.get("https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?sender_device_id=1&talker_id=351201307&session_type=1&size=20&begin_seqno=605&build=0&mobi_app=web",headers=headers)
    return fa.text
