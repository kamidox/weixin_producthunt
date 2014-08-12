# -*- coding: utf-8 -*-

APP_SECRET_KEY = 'your app secret key' #use os.urandom(24) to generate a key.
APP_TOKEN = 'producthunt'

# weixin message template
HELP_INFO = \
u"""
欢迎关注producthut
我们每天定时推送producthunt.com上的产品列表
让你和全球最新鲜出炉的互联网产品零距离接触

Welcome to producthunt
The best new products, every day
"""

HELP_INFO_CUTE = \
u"""
我还在成长中，别调戏我啦 *_*
我相信只要我们足够坚持与专注，一颗幼苗也能成长为参天大树
欢迎给我们提意见：http://weibo.com/smartfoxstudio
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
