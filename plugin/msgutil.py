from re import M
import re
import time
import requests
import demjson
import io
from PIL import Image


class MsgUtil:
    
    headers = {}
    csrf_token = ''
    robotUid = ''

    def __init__(self,headers,csrf_token,robotUid):
        self.headers = headers
        self.csrf_token = csrf_token
        self.robotUid = robotUid
    
    '''
    发送信息
    @MSG 消息
    @suid 发信UID
    @ruid 收信UID
    @return 返回信息
    '''
    def sendMsg(self,Msg,suid,ruid):
        Msg = Msg.replace("﻿","")
        thisTime = time.time()
        postJson = '{"content":"' + str(Msg) + '"}'
        post_data = {'msg[sender_uid]' : suid,'msg[receiver_id]': ruid,'msg[receiver_type]' : 1,'msg[msg_type]':1,'msg[content]':str(postJson),'msg[timestamp]': round(thisTime),'msg[new_face_version]':0,'from_firework': 0,'build': 0,'mobi_app': 'web','csrf_token':self.csrf_token,'csrf' : self.csrf_token,'msg[dev_id]':'10428CA1-33BC-4D9F-9247-62A54251D311','msg[msg_status]':0}
        fa =  requests.post('https://api.vc.bilibili.com/web_im/v1/web_im/send_msg',post_data,headers=self.headers)
        fa.encoding = 'utf-8'
        return fa.text

    '''
    发送图片
    @imageUrl 图片URL -> B站图床
    @suid 发信UID
    @ruid 收信UID
    @width 宽
    @height 高
    @format 格式
    @return 返回信息
    '''
    def sendImage(self,imageUrl,suid,ruid,width,height,format):
        thisTime = time.time()
        postJson = '{"url":"' + str(imageUrl) + '","imageType":"'+str(format)+'","original":1,"height":'+str(height)+',"width":'+str(width)+'}'
        post_data = {'msg[sender_uid]' : suid,'msg[receiver_id]': ruid,'msg[receiver_type]' : 1,'msg[msg_type]':2,'msg[content]':str(postJson),'msg[timestamp]': round(thisTime),'msg[new_face_version]':0,'from_firework': 0,'build': 0,'mobi_app': 'web','csrf_token':self.csrf_token,'csrf' : self.csrf_token,'msg[dev_id]':'10428CA1-33BC-4D9F-9247-62A54251D311','msg[msg_status]':0}
        fa =  requests.post('https://api.vc.bilibili.com/web_im/v1/web_im/send_msg',post_data,headers=self.headers)
        fa.encoding = 'utf-8'
        return fa.text

    '''
    阅读信息 -> 目前一口气给B站上传，代表你已读信息 我并不清楚是否多余请求，请其他开发者指正
    @Mid 读取私信用户UID
    @csrf_token 鉴权值
    @return 返回信息
    '''
    def updateAck(self,Mid,csrf_token):
        post_data = {'talker_id':Mid,'session_type':1,'ack_seqno':195,'build':0,'mobi_app':"web","csrf_token":self.csrf_token,"csrf":self.csrf_token}
        fa =  requests.post('https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack',post_data,headers=self.headers)
        requests.get("https://api.vc.bilibili.com/link_setting/v1/link_setting/is_limit?uid="+str(Mid)+"&type=1",headers=self.headers)
        requests.get("https://api.vc.bilibili.com/link_setting/v1/link_setting/get_session_ss?talker_uid=351201307&build=0&mobi_app=web",headers=self.headers)
        requests.get("https://message.bilibili.com/api/msg/query.room.list.do?page_no=1&mid="+str(Mid),headers=self.headers)
        requests.get("https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?sender_device_id=1&talker_id="+str(Mid)+"&session_type=1&size=20&begin_seqno=514&build=0&mobi_app=web",headers=self.headers)
        fa.encoding = 'utf-8'
        return fa.text

    '''
    上传图片
    @url 图片URL
    @return 返回信息
    '''
    def captureIamgeUrl(self,url):
        #post的参数
        print(url)
        post_data = {'url':url,"csrf":self.csrf_token}
        fa =  requests.post('https://api.bilibili.com/x/article/creative/article/capture',post_data,headers=self.headers)
        fa.encoding = 'utf-8'
        print(fa.text)
        imageUrlJson = demjson.decode(fa.text)
        if imageUrlJson['code'] == 0:
            imageUrl = imageUrlJson['data']['url']
        else:
            imageUrl = "https://i0.hdslb.com/bfs/album/1453def5c58b7c52041e4e076a5a853e358a53e1.jpg"
        return imageUrl
    
    '''
    图片信息获取
    @url 图片URL
    @return 返回信息
    '''

    def getImageFormat(self,url):
        #打开远程图片
        response = requests.get(url)
        #读取储存在内存中的字符串
        tmpIm = io.BytesIO(response.content)
        im = Image.open(tmpIm)
        #在这里返回 一个数组 长 宽 高 格式
        ImageFormat = [im.width,im.height,im.format]
        return ImageFormat
        
    pass