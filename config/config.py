class Config:
    # 机器人发信headers
    HEADERS = {
        "referer": "https://message.bilibili.com/",
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
        'cookie': "COOKIE"
    }
    # B站账号鉴权 -> cookie 的 bili_jct
    CSRF_TOKEN = 'bili_jct'

    # 机器人UID
    ROBOT_UID = 10086

    # TODO 消息刷新心跳 -> 秒数 建议 在 2 ~ 3 之内 如果设置为 1 代表每位用户1秒内最多可以发送1条消息，可以同时发送 根据需求加快心跳 太低可能会给B站造成负担，请不要低于2
    HEARTBEAT_INTERVAL = 3

    # python词库的使用与否 如果要用webhook去当词库，那么建议不使用python词库 以免重复推送
    PYTHON_DIC_STATE = True

    '''
    webhook配置区域
    在这里设置外部接口，如果你有兴趣可以使用返回值来实现外部通信同样的功能
    比如，webhook向挂钩地址请求后，受请求的一方处理这个值，然后直接返回，返回后python把消息推送给机器人
    你也可以搭配下面的Socke，webhook收消息，Socke发消息
    '''
    # webhook挂钩状态 False则不进行发送
    WEBHOOK_STATE = False

    WEBHOOK_DIC_STATE = False

    # webhook挂钩地址 可设为多个，不要太多 即使我已经使用了线程操作
    WEBHOOK_URLS = [
        'https://api.misakaloli.com/api/misaka/WebHook.php'
    ]

    '''
    Socke配置区域 目前采用的是UDP
    这里是我专门留出的，外部可以直接向这个地址去发送请求，收到后直接推送给机器人
    '''
    # Socke通信状态 False则不启动服务端
    SOCKET_STATE = False

    # ----------直播机器人设置-----------

    # 直播间的机器人状态
    LIVE_DIC_STATE = False

    # 直播消息心跳时间，同上
    LIVE_HEARTBEAT_INTERVAL = 3

    # 轮询直播间
    LIVE_ID = 312381
