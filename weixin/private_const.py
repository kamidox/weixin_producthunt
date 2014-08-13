# -*- coding: utf-8 -*-

APP_SECRET_KEY = 'your app secret key' #use os.urandom(24) to generate a key.
APP_TOKEN = 'producthunt'

# weixin message template
WELCOME_INFO = \
u"""
欢迎关注producthut
我们每天定时推送producthunt.com上的最新产品
让你和全球最新最前沿的互联网产品零距离接触

Welcome to producthunt
The best new products, every day
"""

HELP_INFO = \
u"""
可以在这里直接回复你的建议，我们将尽快回复
欢迎私聊，欢迎调戏*_*
也可关注我们的微博：http://weibo.com/smartfoxstudio
"""

TEXT_MSG_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""
