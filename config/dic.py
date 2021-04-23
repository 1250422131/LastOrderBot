#-*-coding:utf-8-*-
import re
import requests
import demjson
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


#发送文本
def sendText(userMsg,robotUid,senderUid):

    if userMsg =="aaa":
        print(msgutil.sendCard("111",robotUid,senderUid))


    if userMsg == "菜单":
        Msg = '来份萝莉\\n你好 聊天内容\\n御坂网络登录申请'
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
        imageUrl = msgutil.captureIamgeUrl("https://api.dongmanxingkong.com/suijitupian/acg/1080p/index.php")
        imageFormat = msgutil.getImageFormat(imageUrl)
        imageWidth = imageFormat[0]
        imageHeight = imageFormat[1]
        imageFormat = imageFormat[2]
        print(msgutil.sendImage(imageUrl,robotUid,senderUid,imageWidth,imageHeight,imageFormat))
        msgutil.updateAck(senderUid,csrf_token)

    if userMsg == "御坂网络登录申请":
        getMsg = requests.get("https://api.misakaloli.com/bilibili/login.php")
        getMsg.encoding = 'utf-8'
        getMsg = getMsg.text
        LoginJson = demjson.decode(getMsg)
        LoginToken = LoginJson['msg']
        userId = LoginJson['check']
        qrImageUrl = LoginJson['img']
        fileutil.write("哔哩哔哩/用户/" + str(senderUid) + "/","userLoginToken.txt",LoginToken)
        fileutil.write("哔哩哔哩/用户/"+ str(senderUid) + "/","userId.txt",userId)
        imageUrl = msgutil.captureIamgeUrl(qrImageUrl)
        imageFormat = msgutil.getImageFormat(imageUrl)
        imageWidth = imageFormat[0]
        imageHeight = imageFormat[1]
        imageFormat = imageFormat[2]
        Msg = '请使用手机客户端扫码\\n完成登录后发送\\n御坂网络登录完成'
        msgutil.sendMsg(Msg,robotUid,senderUid)
        msgutil.sendImage(imageUrl,robotUid,senderUid,imageWidth,imageHeight,imageFormat)
    
    if userMsg == '御坂网络登录完成':
        LoginToken = fileutil.read("哔哩哔哩/用户/" + str(senderUid) + "/","userLoginToken.txt")
        userId = fileutil.read("哔哩哔哩/用户/"+ str(senderUid) + "/","userId.txt")
        getMsg = requests.get("https://api.misakaloli.com/bilibili/loginNew.php?key="+str(LoginToken)+"&uid="+str(userId)+"")
        getMsg.encoding = 'utf-8'
        getMsg = getMsg.text
        LoginJson = demjson.decode(getMsg)
        LoginMsg = LoginJson['msg']
        if LoginJson['code'] == 0:
            Msg = '登录完成，随后会参与自动直播签到\\n更多功能仍然在开发'
        else:
            Msg = '登录未完成'
        msgutil.sendMsg(Msg+"\\n"+str(LoginMsg),robotUid,senderUid)

    if userMsg == '个人中心':
        userId = fileutil.read("哔哩哔哩/用户/"+ str(senderUid) + "/","userId.txt")
        user = requests.get("https://api.misakaloli.com/bilibili/user.php?uid=" + str(userId))
        user.encoding = 'utf-8'
        userJson = demjson.decode(user.text)
        if userJson['code'] == 0:
            Msg = '用户名称：' + str(userJson['name']) + "\\n用户等级："+str(userJson['level'])+ "\\n入站日期："+str(userJson['jointime'])+ "\\n入硬币数量："+str(userJson['yb'])
            msgutil.sendMsg(Msg,robotUid,senderUid)
        else:
            Msg = userJson['msg']
            msgutil.sendMsg(Msg + "请发送 御坂网络登录申请，或者绑定ID",robotUid,senderUid)
        
    

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


    re2 = re.search('^绑定御坂网络ID .*?$', userMsg)
    if re2:
        MsgRe = re.compile('^绑定御坂网络ID (.*?)$')
        MsgReArray = MsgRe.match(userMsg)
        fileutil.write("哔哩哔哩/用户/"+ str(senderUid) + "/","userId.txt",MsgReArray.group(1))
        print(msgutil.sendMsg("绑定成功\\n发送个人中心检查一下吧",robotUid,senderUid))
        msgutil.updateAck(senderUid,csrf_token)

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