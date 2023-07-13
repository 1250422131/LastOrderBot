import json
import re
import time
import requests
import io
import urllib3
from PIL import Image


class MessageUtil:
    headers = {}
    csrf_token = ''
    robot_uid = ''

    def __init__(self, headers, csrf_token, robot_uid):
        self.headers = headers
        self.csrf_token = csrf_token
        self.robot_uid = robot_uid

    def send_card(self, message, sender_uid, receiver_uid):
        message = message.replace("﻿", "")
        current_time = time.time()
        post_json = '{"rid":8580919,"title":"【B站番剧/视频下载】BILIBILI AS v1.0.7更新","summary":"BILIBILI AS是一款基于B站的，开源的，视频/番剧下载Android程序，方便手机用户直接在手机下载视频，专门为手机用户打造的程序！！！它具有解析灵活支持分P等功能，支持直接在B站分享到APP解析。本次更新主要修复了之前一些版本的BUG和新增了些快捷分享解析功能，文章底部有下载地址，我们将在这篇文章一一道来，实现了许多新的功能，还简单调整了一下UI布局，调整对比色（虽然看起来还是那么不和谐），接下来的更新将在高二会考结束后继续。本程序未得到B站官方许可，官方对此概不负责！！！严禁商业，违","author":"萌新杰少","view":1833,"like":82,"reply":51,"template_id":4,"image_urls":["https://i0.hdslb.com/bfs/article/f7985db6804a0782bdad3248540431d27be9f347.jpg"]}'
        post_data = {'msg[sender_uid]': sender_uid, 'msg[receiver_id]': receiver_uid, 'msg[receiver_type]': 1, 'msg[msg_type]': 12,
                     'msg[content]': str(post_json), 'msg[timestamp]': round(current_time), 'msg[new_face_version]': 0,
                     'from_firework': 0, 'build': 0, 'mobi_app': 'web', 'csrf_token': self.csrf_token,
                     'csrf': self.csrf_token, 'msg[dev_id]': '10428CA1-33BC-4D9F-9247-62A54251D311',
                     'msg[msg_status]': 0, 'msg[msg_seqno]': 0}
        response = requests.post('https://api.vc.bilibili.com/web_im/v1/web_im/send_msg', post_data, headers=self.headers)
        response.encoding = 'utf-8'
        return response.text

    def send_message(self, message, sender_uid, receiver_uid):
        message = message.replace("﻿", "")
        current_time = time.time()
        post_json = '{"content":"' + str(message) + '"}'
        post_data = {'msg[sender_uid]': sender_uid, 'msg[receiver_id]': receiver_uid, 'msg[receiver_type]': 1, 'msg[msg_type]': 1,
                     'msg[content]': str(post_json), 'msg[timestamp]': round(current_time), 'msg[new_face_version]': 0,
                     'from_firework': 0, 'build': 0, 'mobi_app': 'web', 'csrf_token': self.csrf_token,
                     'csrf': self.csrf_token, 'msg[dev_id]': '10428CA1-33BC-4D9F-9247-62A54251D311',
                     'msg[msg_status]': 0}
        response = requests.post('https://api.vc.bilibili.com/web_im/v1/web_im/send_msg', post_data, headers=self.headers)
        response.encoding = 'utf-8'
        return response.text

    def send_image(self, image_url, sender_uid, receiver_uid, width, height, image_format):
        current_time = time.time()
        post_json = '{"url":"' + str(image_url) + '","imageType":"' + str(image_format) + '","original":1,"height":' + str(
            height) + ',"width":' + str(width) + '}'
        post_data = {'msg[sender_uid]': sender_uid, 'msg[receiver_id]': receiver_uid, 'msg[receiver_type]': 1, 'msg[msg_type]': 2,
                     'msg[content]': str(post_json), 'msg[timestamp]': round(current_time), 'msg[new_face_version]': 0,
                     'from_firework': 0, 'build': 0, 'mobi_app': 'web', 'csrf_token': self.csrf_token,
                     'csrf': self.csrf_token, 'msg[dev_id]': '10428CA1-33BC-4D9F-9247-62A54251D311',
                     'msg[msg_status]': 0}
        response = requests.post('https://api.vc.bilibili.com/web_im/v1/web_im/send_msg', post_data, headers=self.headers)
        response.encoding = 'utf-8'
        return response.text

    def update_ack(self, mid, csrf_token):
        post_data = {'talker_id': mid, 'session_type': 1, 'ack_seqno': 195, 'build': 0, 'mobi_app': "web",
                     "csrf_token": self.csrf_token, "csrf": self.csrf_token}
        response = requests.post('https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack', post_data,
                                 headers=self.headers)
        response.encoding = 'utf-8'
        return response.text

    def capture_image_url(self, url):
        print(url)
        post_data = {'url': url, "csrf": self.csrf_token}
        response = requests.post('https://api.bilibili.com/x/article/creative/article/capture', post_data,
                                 headers=self.headers)
        response.encoding = 'utf-8'
        print(response.text)
        image_url_json = json.load(response.text)
        if image_url_json['code'] == 0:
            image_url = image_url_json['data']['url']
        else:
            image_url = "https://i0.hdslb.com/bfs/album/1453def5c58b7c52041e4e076a5a853e358a53e1.jpg"
        return image_url

    def upcover_image(self, url):
        image_name = 'binary'
        data_param = {"csrf": self.csrf_token, 'img_name': image_name}
        image_file = io.StringIO(urllib3.urlopen(url).read())
        image_data = Image.open(image_file)
        output = io.BytesIO()
        image_data.save(output, format='PNG')
        print(image_data.format)
        image_data.close()
        data_bin = output.getvalue()
        output.close()
        file_obj = data_bin
        img_file = {image_name: file_obj}
        data_result = requests.post(url, data_param, files=img_file, headers=self.headers)
        if isinstance(file_obj, MessageUtil):
            file_obj.close()
        data_result_json = json.decode(data_result)
        if data_result_json['code'] == 0:
            image_url = data_result_json['data']['url']
        else:
            image_url = "https://i0.hdslb.com/bfs/album/1453def5c58b7c52041e4e076a5a853e358a53e1.jpg"
        return image_url

    def get_image_format(self, url):
        response = requests.get(url)
        tmp_image = io.BytesIO(response.content)
        image = Image.open(tmp_image)
        image_format = [image.width, image.height, image.format]
        return image_format

    def send_message_in_live(self, message, room_id):
        message = message.replace("﻿", "")
        current_time = time.time()
        post_data = {'msg': message, 'roomid': room_id, 'bubble': 0, 'color': 16777215, 'fontsize': 25, 'mode': 1,
                     'rnd': round(current_time), 'csrf': self.csrf_token, 'csrf_token': self.csrf_token}
        response = requests.post('https://api.live.bilibili.com/msg/send', post_data, headers=self.headers)
        response.encoding = 'utf-8'
        return response.text
