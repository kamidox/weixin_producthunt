# -*- coding: utf-8 -*-

APP_TOKEN = 'producthunt'
APP_HOST = 'kamidox.com/producthunt/'
APP_DEBUG = True

# database
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'producthunt'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'kamidox'


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
回复下面对应数字获取产品信息：
1. 最近两天得票最多的产品
2. 最近一周得票最多的产品
3. 最近一月得票最多的产品

其他统计功能正在开发中，敬请期待：
1. 评论最多的产品
2. 评论+得票最多的产品
3. 评论+得票+评论点赞最多的产品
还有什么好玩的点子？欢迎反馈信息给我们，一起来玩玩数据挖掘吧。
"""

ERROR_INFO = \
u"""
oops! no data found!
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

ARTICLES_MSG_TPL_HEAD = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
"""

ARTICLES_MSG_TPL_TAIL = \
u"""
</Articles>
</xml>
"""

ARTICLES_ITEM_TPL = \
u"""
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
"""
