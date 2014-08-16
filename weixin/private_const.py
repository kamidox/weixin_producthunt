# -*- coding: utf-8 -*-

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
回复以下数字获取内容：
1.实时信息
2.昨日之最
3.本周之最
4.本用之最
5.深度报导
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
