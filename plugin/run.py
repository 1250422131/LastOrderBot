# -*-coding:utf-8-*-
import json
import requests
import time
import threading
from plugin.msgutil import MessageUtil
from config import dic
from config.config import Config
from socket import *

# 获取全局配置
headers = Config.HEADERS
csrf_token = Config.CSRF_TOKEN
robot_uid = Config.ROBOT_UID
python_dic_state = Config.PYTHON_DIC_STATE
heartbeat_interval = Config.HEARTBEAT_INTERVAL
web_hook_state = Config.WEBHOOK_STATE
web_hook_dic_state = Config.WEBHOOK_DIC_STATE
web_hook_urls = Config.WEBHOOK_URLS
socket_state = Config.SOCKET_STATE
live_heartbeat_interval = Config.LIVE_HEARTBEAT_INTERVAL
live_id = Config.LIVE_ID
live_dic_state = Config.LIVE_DIC_STATE
msg_util = MessageUtil(headers, csrf_token, robot_uid)


def run():
    # 启动一个线程，后台介绍信息，使得后续机器人可正常检测内容
    if socket_state:
        web_hook_thread = threading.Thread(target=robot_socket)
        web_hook_thread.start()

    if live_dic_state:
        live_thread = threading.Thread(target=live_broadcast_run)
        live_thread.start()

    while True:
        time.sleep(heartbeat_interval)
        this_time = time.time()
        this_time = round(this_time * 1000000)
        this_heartbeat_interval = heartbeat_interval - 0.2
        past_time = round(this_heartbeat_interval * 1000000)
        this_time = int(this_time) - past_time
        new_msg_get = requests.get(
            "https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?begin_ts=" + str(
                this_time) + "&build=0&mobi_app=web", headers=headers)
        new_msg_get.encoding = 'utf-8'
        new_msg = json.load(new_msg_get.text)

        if bool("session_list" in str(new_msg)) and not ("'session_list': None" in str(new_msg)):
            i = 0
            while i < len(new_msg['data']['session_list']):
                new_msg_json = new_msg['data']['session_list'][i]
                receiver_id = new_msg_json["last_msg"]["receiver_id"]
                sender_uid = new_msg_json["last_msg"]['sender_uid']
                unread_count = new_msg_json["unread_count"]
                ack_seqno = int(new_msg_json["max_seqno"])

                if robot_uid == int(receiver_id):
                    dic.update_ack(sender_uid, ack_seqno, csrf_token)
                    web_hook_thread = threading.Thread(target=web_hook, args=(new_msg, 1))
                    web_hook_thread.start()

                    if python_dic_state:
                        msg_type = new_msg_json["last_msg"]["msg_type"]

                        if unread_count >= 1:
                            if msg_type == 1:
                                msg_json = json.load(new_msg_json["last_msg"]["content"])
                                msg = msg_json['content']
                                dic.send_text(msg, receiver_id, sender_uid)
                            elif msg_type == 2:
                                image_json = json.load(new_msg_json["last_msg"]["content"])
                                dic.send_image(image_json, receiver_id, sender_uid)
                        elif unread_count == 0:
                            if msg_type == 1:
                                msg_json = json.load(new_msg_json["last_msg"]["content"])
                                msg = msg_json['content']
                                dic.withdraw_text(msg, receiver_id, sender_uid)
                            elif msg_type == 2:
                                print(new_msg_json["last_msg"]["content"])
                                image_json = json.load(new_msg_json["last_msg"]["content"])
                                dic.withdraw_image(image_json, receiver_id, sender_uid)
                i = i + 1
        else:
            pass


def web_hook(new_json, key):
    if web_hook_state:
        headers = {
            'Connection': 'close',
            'Content-Type': 'application/json;charset=UTF-8'
        }
        i = 0
        while i < len(web_hook_urls):
            web_hook_msg_str = requests.post(url=web_hook_urls[i], data=json.dumps(new_json), headers=headers)

            if web_hook_dic_state:
                msg_json = json.load(web_hook_msg_str.text)
                print(msg_json)
                msg = msg_json["msg"]
                msg_type = msg_json["msg_type"]
                receiver_id = msg_json["receiverid"]
                sender_uid = msg_json["senderuid"]
                print(msg_type)
                if msg_type == 1:
                    print(msg_util.send_message(msg, sender_uid, receiver_id))
                elif msg_type == 2:
                    image_url = msg_util.capture_image_url(msg)
                    image_format = msg_util.get_image_format(image_url)
                    image_width = image_format[0]
                    image_height = image_format[1]
                    image_format = image_format[2]
                    msg_util.send_image(image_url, sender_uid, receiver_id, image_width, image_height, image_format)
                pass
            i = i + 1


def robot_socket():
    print("==============RobotUDP服务端已经启动===================")
    host = '127.0.0.1'
    port = 2233
    bufsiz = 1024
    addr = (host, port)
    udp_ser_sock = socket(AF_INET, SOCK_DGRAM)
    udp_ser_sock.bind(addr)

    while True:
        print('等待接收消息...')
        data, addr = udp_ser_sock.recvfrom(bufsiz)
        msg_json = json.load(data)
        msg = msg_json["msg"]
        msg_type = msg_json["msg_type"]
        receiver_id = msg_json["receiverid"]
        sender_uid = msg_json["senderuid"]
        print(msg_type)
        if msg_type == 1:
            print(msg_util.send_message(msg, sender_uid, receiver_id))
        elif msg_type == 2:
            image_url = msg_util.capture_image_url(msg)
            image_format = msg_util.get_image_format(image_url)
            image_width = image_format[0]
            image_height = image_format[1]
            image_format = image_format[2]
            msg_util.send_image(image_url, sender_uid, receiver_id, image_width, image_height, image_format)
        udp_ser_sock.sendto(bytes(data.decode('utf-8'), 'utf-8'), addr)
        print('响应消息到', addr)

    udp_ser_sock.close()


def live_broadcast_run():
    msg_dictionary = []
    max_count = 1000
    while True:
        time.sleep(live_heartbeat_interval)
        new_msg_get = requests.get(
            "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid=" + str(live_id),
            headers=headers)
        new_msg_get.encoding = 'utf-8'
        new_msg = json.load(new_msg_get.text)
        room_array_json = new_msg['data']['room']
        i = 0
        while i < len(room_array_json):
            msg_data = room_array_json[i]
            msg_time = msg_data['check_info']['ct']
            msg = msg_data['text']
            uid = msg_data['uid']

            if int(uid) != robot_uid:
                if len(room_array_json) < len(msg_dictionary):
                    if msg_time in msg_dictionary:
                        pass
                    else:
                        msg_dictionary.append(msg_time)
                        dic.live_send_text(msg, live_id)

                        if len(msg_dictionary) > max_count:
                            del msg_dictionary[0:max_count - 10]
                            pass
                else:
                    msg_dictionary.append(msg_time)
            i = i + 1
