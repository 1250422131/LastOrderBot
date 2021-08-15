import json
from re import M
import re
import time
import requests
import demjson
import io
import urllib3
from PIL import Image


class MsgUtil:
    
    headers = {}
    csrf_token = ''
    robotUid = ''

    def __init__(self,headers,csrf_token,robotUid):
        self.headers = headers
        self.csrf_token = csrf_token
        self.robotUid = robotUid

    def sendCard(self,Msg,suid,ruid):
        Msg = Msg.replace("﻿","")
        thisTime = time.time()
        postJson = '{"rid":8580919,"title":"【B站番剧/视频下载】BILIBILI AS v1.0.7更新","summary":"BILIBILI AS是一款基于B站的，开源的，视频/番剧下载Android程序，方便手机用户直接在手机下载视频，专门为手机用户打造的程序！！！它具有解析灵活支持分P等功能，支持直接在B站分享到APP解析。本次更新主要修复了之前一些版本的BUG和新增了些快捷分享解析功能，文章底部有下载地址，我们将在这篇文章一一道来，实现了许多新的功能，还简单调整了一下UI布局，调整对比色（虽然看起来还是那么不和谐），接下来的更新将在高二会考结束后继续。本程序未得到B站官方许可，官方对此概不负责！！！严禁商业，违","author":"萌新杰少","view":1833,"like":82,"reply":51,"template_id":4,"image_urls":["https://i0.hdslb.com/bfs/article/f7985db6804a0782bdad3248540431d27be9f347.jpg"]}'
        post_data = {'msg[sender_uid]' : suid,'msg[receiver_id]': ruid,'msg[receiver_type]' : 1,'msg[msg_type]':12,'msg[content]':str(postJson),'msg[timestamp]': round(thisTime),'msg[new_face_version]':0,'from_firework': 0,'build': 0,'mobi_app': 'web','csrf_token':self.csrf_token,'csrf' : self.csrf_token,'msg[dev_id]':'10428CA1-33BC-4D9F-9247-62A54251D311','msg[msg_status]':0,'msg[msg_seqno]':0}
        fa =  requests.post('https://api.vc.bilibili.com/web_im/v1/web_im/send_msg',post_data,headers=self.headers)
        fa.encoding = 'utf-8'
        return fa.text
    
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


    def upcoverImage(self,url):

        image_name = 'binary'
        data_param= {"csrf":self.csrf_token,'img_name': image_name} #有些API要求指定文件名参数
        # TODO 获取远程网络图片
        image_file = io.StringIO(urllib3.urlopen(url).read())
        image_data = Image.open(image_file)
        output = io.BytesIO()
        image_data.save(output, format='PNG') # format=image_data.format
        print (image_data.format) #输出的不一定是JPEG也可能是PNG
        image_data.close()
        data_bin = output.getvalue()
        output.close()
        file_obj = data_bin
        #fixed at 2017-05-19 10:49:57
        img_file= {image_name: file_obj} #Very Important. 
        #the key must be the filename, 
        #because the requests cannot guess the correct filename from the bytes array.
        data_result = requests.post(url, data_param, files=img_file ,headers=self.headers)
        if isinstance(file_obj, MsgUtil): #这里load_image获得的是二进制流了，不是file对象。
            file_obj.close()
        data_resultJson = demjson.decode(data_result)
        if data_resultJson['code'] == 0:
            imageUrl = data_resultJson['data']['url']
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


    # TODO 直播区功能
    '''
    发送信息
    @MSG 消息
    @roomid 收信直播间ID
    @return 返回信息
    '''

    #$str = $BilibiliClass->bilibiliPost($_GET['uid'], "msg=" . $msg . "&roomid=" . $id . "&bubble=0&color=16777215&fontsize=25&mode=1&csrf=" . $token . "&rnd=" . $time . "&csrf_token=" . $token, $url);
    def liveSendMsg(self,Msg,rommid):
        Msg = Msg.replace("﻿","")
        thisTime = time.time()
        post_data = {'msg' : Msg,'roomid': rommid,'bubble' : 0,'color':16777215,'fontsize':25,'mode': 1,'rnd':round(thisTime),'csrf':self.csrf_token,'csrf_token' : self.csrf_token}
        fa =  requests.post('https://api.live.bilibili.com/msg/send',post_data,headers=self.headers)
        fa.encoding = 'utf-8'
        return fa.text
        
    pass