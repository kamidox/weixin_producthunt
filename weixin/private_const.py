# -*- coding: utf-8 -*-

APP_TOKEN = 'producthunt'
APP_HOST = 'http://kamidox.com'
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
The best new products, every day, in wechat

"""

HELP_INFO = \
u"""
回复下面命令获取产品信息：
dtv - day_top_voted
最近两天得票最多的产品
wtv - week_top_voted
最近一周得票最多的产品
mtv - month_top_voted
最近一月得票最多的产品

dtc - day_top_comments
最近两天评论最多的产品
wtc - week_top_comments
最近一周评论最多的产品
mtc - month_top_comments
最近一月评论最多的产品

dtcv - day_top_comment_voted
最近两天评论点赞最多的产品
wtcv - week_top_comment_voted
最近一周评论点赞最多的产品
mtcv - month_top_comment_voted
最近一月评论点赞最多的产品

search:keyword
搜索包含keyword的相关产品

Try following commands:
dtv - day_top_voted
top voted products in these two days
wtv - week_top_voted
top voted products in this week
mtv - month_top_voted
top voted products in this month

dtc - day_top_comments
top comments products in these two days
wtc - week_top_comments
top comments products in this week
mtc - month_top_comments
top comments products in this month

dtcv - day_top_comment_voted
top comments voted(cv) products in these two days
wtcv - week_top_comment_voted
top comments voted(cv) products in this week
mtcv - month_top_comment_voted
top comments voted(cv) products in this month

search:keyword
search products base on keyword
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
