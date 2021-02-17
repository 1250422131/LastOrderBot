#在这里配置你的机器人操作类中需要的东西，图方便就不写JSON了，大家这样也好理解
class Config:

    #机器人发信headers
    headers = {
    "referer": "https://message.bilibili.com/",
    'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    'cookie' : "l=v; _uuid=AAD30B35-4DEC-B7F6-B45C-9710D18A803E12182infoc; buvid3=FB49D4DF-4C5E-4F40-A09A-07ECC94EECA253945infoc; LIVE_BUVID=AUTO6115851179352483; CURRENT_FNVAL=16; rpdid=|(~u|)Jll~R0J'ul)luumu|m; PVID=1; fingerprint=97ae40aa6d241dbca486f9072353c9c4; buvid_fp=FB49D4DF-4C5E-4F40-A09A-07ECC94EECA253945infoc; buvid_fp_plain=FB49D4DF-4C5E-4F40-A09A-07ECC94EECA253945infoc; bp_t_offset_351201307=491287513561068540; bp_t_offset_515959494=488278223245354175; SESSDATA=73af3ec9%2C1629000066%2Cad04e%2A21; bili_jct=38c4a689ad2b54b9ede35196794133a9; DedeUserID=352652749; DedeUserID__ckMd5=a0e23efaa3cabc18; sid=8lf5g4mc"
    }

    #B站账号鉴权 -> cookie 的 bili_jct
    csrf_token = '38c4a689ad2b54b9ede35196794133a9'

    #机器人UID
    robot_uid = 352652749

    # TODO 消息刷新心跳 -> 秒数 建议 在 0.5 ~ 3 之内 如果设置为 1 代表每位用户1秒内最多可以发送1条消息，可以同时发送 根据需求加快心跳 太低可能会给B站造成负担，请不要低于0.5
    heartbeat_interval = 1

