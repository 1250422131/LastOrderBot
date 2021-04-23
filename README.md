# LastOrderBot
 LastOrderBot是一款B站机器人
 使用**LastOrderBot**可以帮助你轻松搭建属于自己的B站机器人

### 功能
 目前**LastOrderBot**支持的功能如下
 - 正在开发的功能
 - [ ] 明文或其他方式登录
 - [x] 收发文本信息
 - [x] 收发网络图片信息
 - [x] 收发直播间文本信息
 - [ ] 收发直播间礼物功能
 - [x] 接收撤回文本及图片信息
 - [x] 设置心跳【信息接受间隔】
 - [x] 机器人和用户同时使用账号
 - [ ] 本地图片发送
 - [ ] 撤回自己的消息
 - [x] 其他语言词库支持
 - [x] WebHook
 - [x] Socke通信


### WebHook介绍
 为了方便大家进行更多的功能配置，我为大家留出了webhook

 webhook的功能你可以百度知道

 当机器人收到消息后回向webhook设置的地址主动请求，推送信息

 你可以在run.py找到原理 记得在**config.py**打开配置

  ```php
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
        'receiverid' => $receiverid,
        'senderuid' => $senderUid,
        'msg' => $Msg
    ];
    echo json_encode($array, JSON_UNESCAPED_UNICODE);
  ```

### 安装教程
 安装过程虽然简单，但是我已经在博客发过了，就不再阐述了，下面是地址
 
 [**LastOrderBot安装方案**](https://imcys.com/2021/02/19/b%e7%ab%99%e6%9c%ba%e5%99%a8%e4%ba%ba%e6%90%ad%e5%bb%ba-lastorderbot.html)

### 配置介绍
 下面我简单阐述下机器人相关配置

 打开 config 的 config.py

 在这里配置机器人相关信息，切记一定要看注释配置

 这里的心跳是指x秒内检测一下新消息，同一个用户最多只能在这个时间内给机器人发送1条消息，多出则检测最新的，后面会修复这个问题