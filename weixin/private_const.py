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
欢迎关注producthut
我们每天定时推送producthunt.com上的最新产品
让你和全球最新最前沿的互联网产品零距离接触
"""

HELP_INFO = \
u"""
回复数字获取产品信息：
1 - 最近两天得票最多的产品
2 - 最近一周得票最多的产品
3 - 最近一月得票最多的产品

4 - 最近两天评论最多的产品
5 - 最近一周评论最多的产品
6 - 最近一月评论最多的产品

7 - 最近两天评论点赞最多的产品
8 - 最近一周评论点赞最多的产品
9 - 最近一月评论点赞最多的产品

搜索包含keyword的相关产品
search:keyword
"""

ERROR_INFO = \
u"""
oops! no data found!
"""

WX_TEXT_TPL = \
u"""
[%sV]<a href=%s>%s</a>
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
