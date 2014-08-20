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
我们的后台程序正在开发中，相关功能即将推出，敬请期待
首期规划功能：
实时信息：实时显示当天producthunt.com上的产品及评论
昨日之最：昨日评分最高的五个产品及其精彩评论
本周之最：本周评分最高的十个产品及其精彩评论
本月之最：本月评分最高的十个产品及其精彩评论

还有什么好玩的点子？一直来玩玩数据挖掘吧。比如评论最多的产品是哪个？所有评论点赞最多的产品是哪个？
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
