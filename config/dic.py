import json
import re
import requests
from plugin.msgutil import MessageUtil
from config.config import Config
from plugin.fileutil import FileUtil

headers = Config.HEADERS
csrf_token = Config.CSRF_TOKEN
robot_uid = Config.ROBOT_UID
msg_util = MessageUtil(headers, csrf_token, robot_uid)
file_util = FileUtil()


# DIC词库内容
# update_ack新版本直接在消息获取时完成，以后可以不加入


# 发送文本
def send_text(user_msg, robot_uid, sender_uid):
    if user_msg == "菜单":
        msg = '来份萝莉\\n你好 聊天内容\\n御坂网络登录申请\\nBig图片降噪\\n原神模块'
        print(msg_util.send_message(msg, robot_uid, sender_uid))

    # 字符串匹配
    if user_msg == "你好":
        msg = "你也好"
        # 发送者UID 接受UID
        print(msg_util.send_message(msg, robot_uid, sender_uid))

    if user_msg == "你是不是萝莉":
        msg = '不不不，我想不是'
        print(msg_util.send_message(msg, robot_uid, sender_uid))

    if user_msg == "来份萝莉":
        image_url = msg_util.upcover_image("https://api.dongmanxingkong.com/suijitupian/acg/1080p/index.php")
        image_format = msg_util.get_image_format(image_url)
        image_width = image_format[0]
        image_height = image_format[1]
        image_format = image_format[2]
        print(msg_util.send_image(image_url, robot_uid, sender_uid, image_width, image_height, image_format))
        msg_util.update_ack(sender_uid, csrf_token)

    # 正则表达式区域
    re1 = re.search('^你好 ?(.*?)$', user_msg)
    if re1:
        msg_re = re.compile('^你好 ?(.*?)$')
        msg_re_array = msg_re.findall(user_msg)
        print(msg_re_array[0])
        get_msg = requests.get("http://i.itpk.cn/api.php?question=" + str(
            msg_re_array[0]) + "&api_key=45c0866382610cbee9bbbffaef5aa943&api_secret=ffnzr6hrzzaj&limit=8")
        get_msg.encoding = 'utf-8'
        get_msg = get_msg.text
        print(msg_util.send_message(get_msg, robot_uid, sender_uid))
        msg_util.update_ack(sender_uid, csrf_token)

    if re.search('^原神游戏公告 ?(.*?)$', user_msg):
        msg_re = re.compile('^原神游戏公告 ?(.*?)$')
        msg_re_array = msg_re.findall(user_msg)

        get_msg = requests.get(
            "https://pan.misakaloli.com/api/mihuyou/?form=game&type=getData&id=" + str(msg_re_array[0])).text
        game_json = json.loads(get_msg)
        print(game_json)
        image_url = game_json['imageurl']
        activity_url = game_json['activityUrl']
        # 直接上传文件文件

        # 图片发送失败时用下载上传，代码如下
        image_url = msg_util.upcover_image(image_url)
        image_format = msg_util.get_image_format(image_url)
        image_width = image_format[0]
        image_height = image_format[1]
        image_format = image_format[2]
        msg_util.send_image(image_url, robot_uid, sender_uid, image_width, image_height, image_format)

        msg_util.send_message("详细信息如下\\n" + str(activity_url), robot_uid, sender_uid)

    if re.search('^原神活动公告 ?(.*?)$', user_msg):
        msg_re = re.compile('^原神活动公告 ?(.*?)$')
        msg_re_array = msg_re.findall(user_msg)

        get_msg = requests.get(
            "https://pan.misakaloli.com/api/mihuyou/?form=activity&type=getData&id=" + str(msg_re_array[0])).text
        game_json = json.loads(get_msg)
        image_url = game_json['imageurl']
        activity_url = game_json['activityUrl']
        print(game_json)

        image_url = msg_util.capture_image_url(image_url)
        image_format = msg_util.get_image_format(image_url)
        image_width = image_format[0]
        image_height = image_format[1]
        image_format = image_format[2]
        msg_util.send_image(image_url, robot_uid, sender_uid, image_width, image_height, image_format)

        msg_util.send_message("详细信息如下\\n" + str(activity_url), robot_uid, sender_uid)


# 发送图片
def send_image(image_json, receiver_id, sender_uid):
    image_url = image_json['url']
    image_type = image_json['imageType']
    image_height = image_json['height']
    image_width = image_json['width']

    msg = '图片地址：' + image_url + '\\n图片格式：' + image_type
    print(msg_util.send_message(msg, robot_uid, sender_uid))
    msg_util.update_ack(sender_uid, csrf_token)
    # 这里我给个建议，先让用户发送指令，机器人把数据记录一下，然后判断如果下面有这个记录，做相应操作就可以


# 发现撤回文本
def withdraw_text(user_msg, robot_uid, sender_uid):
    msg = '检测到你撤回了内容：' + user_msg
    print(msg_util.send_message(msg, robot_uid, sender_uid))
    msg_util.update_ack(sender_uid, csrf_token)


# 发现撤回图片
def withdraw_image(image_json, receiver_id, sender_uid):
    image_url = image_json['url']
    image_type = image_json['imageType']
    image_height = image_json['height']
    image_width = image_json['width']

    msg = '检测到撤回了图片\\n图片地址：' + image_url + '\\n图片格式：' + image_type
    print(msg_util.send_message(msg, robot_uid, sender_uid))
    msg_util.update_ack(sender_uid, csrf_token)
    pass


'''
阅读信息 -> 目前一口气给B站上传，代表你已读信息 我并不清楚是否多余请求，请其他开发者指正
@Mid 读取私信用户UID
@csrf_token 鉴权值
 @return 返回信息
'''


def update_ack(mid, ack_seqno, csrf_token):
    post_data = {'talker_id': mid, 'session_type': 1, 'ack_seqno': ack_seqno, 'build': 0, 'mobi_app': "web",
                 "csrf_token": csrf_token, "csrf": csrf_token}
    fa = requests.post('https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack', post_data, headers=headers)
    return fa.text


# 直播文本发送
def live_send_text(user_msg, rommid):
    if user_msg == "测试":
        # 发送直播消息
        msg_util.send_message_in_live("你好，我是御坂妹妹", rommid)

    # 正则表达式区域
    re1 = re.search('^你好 ?(.*?)$', user_msg)
    if re1:
        msg_re = re.compile('^你好 ?(.*?)$')
        msg_re_array = msg_re.findall(user_msg)
        print(msg_re_array[0])
        get_msg = requests.get("http://i.itpk.cn/api.php?question=" + str(
            msg_re_array[0]) + "&api_key=45c0866382610cbee9bbbffaef5aa943&api_secret=ffnzr6hrzzaj&limit=8")
        get_msg.encoding = 'utf-8'
        get_msg = get_msg.text
        print(msg_util.send_message_in_live(get_msg, rommid))
