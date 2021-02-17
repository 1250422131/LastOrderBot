#在这里配置你的机器人操作类中需要的东西，图方便就不写JSON了，大家这样也好理解
class Config:

    #机器人发信headers
    headers = {
    "referer": "https://message.bilibili.com/",
    'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    'cookie' : "你的cooike"
    }

    #B站账号鉴权 -> cookie 的 bili_jct
    csrf_token = 'bili_jct'

    #机器人UID
    robot_uid = 10086

    # TODO 消息刷新心跳 -> 秒数 建议 在 0.5 ~ 3 之内 如果设置为 1 代表每位用户1秒内最多可以发送1条消息，可以同时发送 根据需求加快心跳 太低可能会给B站造成负担，请不要低于0.5
    heartbeat_interval = 1

