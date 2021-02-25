# LastOrderBot
 LastOrderBot是一款B站机器人
 使用**LastOrderBot**可以帮助你轻松搭建属于自己的B站机器人

### 功能
 目前**LastOrderBot**支持的功能如下
 * 明文或其他方式登录 ×
 * 接收文本信息 √
 * 接收图片信息 √
 * 接收撤回文本及图片信息 √
 * 设置心跳【信息接受间隔】 √
 * 机器人和用户同时使用账号 √

### 安装教程
 安装过程虽然简单，但是我已经在博客发过了，就不再阐述了，下面是地址
 
 [**LastOrderBot安装方案**](https://imcys.com/2021/02/19/b%e7%ab%99%e6%9c%ba%e5%99%a8%e4%ba%ba%e6%90%ad%e5%bb%ba-lastorderbot.html)

### 配置介绍
 下面我简单阐述下机器人相关配置

 打开 config 的 config.py

 在这里配置机器人相关信息，切记一定要看注释配置

 这里的心跳是指x秒内检测一下新消息，同一个用户最多只能在这个时间内给机器人发送1条消息，多出则检测最新的，后面会修复这个问题
 ```python
 #在这里配置你的机器人操作类中需要的东西，图方便就不写JSON了，大家这样也好理解
 class Config:

    #机器人发信headers
    headers = {
    "referer": "https://message.bilibili.com/",
    'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    'cookie' : "你的cookie"
    }

    #B站账号鉴权 -> cookie 的 bili_jct
    csrf_token = 'bili_jct'

    #机器人UID
    robot_uid = 10086

    # TODO 消息刷新心跳 -> 秒数 建议 在 0.5 ~ 3 之内 如果设置为 1 代表每位用户1秒内最多可以发送1条消息，可以同时发送 根据需求加快心跳 太低可能会给B站造成负担，请不要低于0.5
    heartbeat_interval = 1

 ```


