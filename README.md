# LastOrderBot
 LastOrderBot是一款B站机器人
 使用**LastOrderBot**可以帮助你轻松搭建属于自己的B站机器人

### 功能
 目前**LastOrderBot**支持的功能如下
 - 正在开发的功能
 - [ ] 明文或其他方式登录
 - [x] 收发文本信息
 - [x] 收发网络图片信息
 - [x] 接收撤回文本及图片信息
 - [x] 设置心跳【信息接受间隔】
 - [x] 机器人和用户同时使用账号
 - [x] 接收撤回文本及图片信息
 - [ ] 本地图片发送
 - [ ] 撤回自己的消息
 - [x] 其他语言词库支持
 - [x] WebHook
 - [x] Socke通信


### WebHook介绍
 为了方便大家进行更多的功能配置，我为大家留出了webhook
 webhook的功能你可以百度知道
 当机器人收到消息后回向webhook设置的地址主动请求，推送信息

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
 #在这里配置你的机器人操作类中需要的东西，图方便就不写JSON了，大家这样也好理解
class Config:

    # 机器人发信headers
    headers = {
    "referer": "https://message.bilibili.com/",
    'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    'cookie' : "你的cookie"
    }
    # B站账号鉴权 -> cookie 的 bili_jct
    csrf_token = 'bili_jct'

    # 机器人UID
    robot_uid = 2233

    # TODO 消息刷新心跳 -> 秒数 建议 在 0.5 ~ 3 之内 如果设置为 1 代表每位用户1秒内最多可以发送1条消息，可以同时发送 根据需求加快心跳 太低可能会给B站造成负担，请不要低于0.5
    heartbeat_interval = 1

    # python词库的使用与否 如果要用webhook去当词库，那么建议不使用python词库 以免重复推送
    pythonDicState = True

    '''
    webhook配置区域
    在这里设置外部接口，如果你有兴趣可以使用返回值来实现外部通信同样的功能
    比如，webhook向挂钩地址请求后，受请求的一方处理这个值，然后直接返回，返回后python把消息推送给机器人
    你也可以搭配下面的Socke，webhook收消息，Socke发消息
    '''
    # webhook挂钩状态 False则不进行发送
    webHookState = False

    webHookDicState = False

    # webhook挂钩地址 可设为多个，不要太多 即使我已经使用了线程操作
    webHookUrl = [
        ''
    ]

    '''
    Socke配置区域 目前采用的是UDP
    这里是我专门留出的，外部可以直接向这个地址去发送请求，收到后直接推送给机器人
    '''
    # Socke通信状态 False则不启动服务端
    SocketState = True
 ```

