# -*- coding: utf-8 -*-

APP_TOKEN = 'producthunt'
APP_ROOT = '/weixin'
APP_HOST = 'http://kamidox.com/weixin'
APP_DEBUG = True

# database
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'producthunt'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'kamidox'


# weixin message template
WELCOME_INFO = \
u"""
终于找到我们啦，不容易呀
我们是一个众包翻译／介绍国外最新的互联网产品的兴趣小组

LET COOL PRODUCTS EMBRACE CHINA!

有关中文产品介绍，请关注每日推送及历史消息
"""

THANKS_INFO = u"""感谢留言，我们将尽快回复"""

HELP_INFO = \
u"""
回复数字获取产品信息：
1 - 最近两天得票最多的产品
2 - 最近一周得票最多的产品
3 - 最近一月得票最多的产品

搜索包含keyword的相关产品
search:keyword

如需中文产品介绍，请关注每日推送及历史消息
"""

ERROR_INFO = \
u"""
oops! no data found!
"""

WX_TEXT_TPL = \
u"""
%s
%s
%s
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
