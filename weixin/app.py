#!/bin/env python
# -*- coding: utf-8 -*-
import hashlib, time
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template
from private_const import *
import view

app = Flask(__name__, static_url_path=APP_ROOT + '/static')
app.debug = APP_DEBUG

#homepage just for fun
@app.route(APP_ROOT + '/')
def home():
    return render_template('index.html')

#homepage just for fun
@app.route(APP_ROOT + '/weixin_test')
def weixin_test():
    p = view.populate_test_data()
    return render_template('comments.jinja.html', product=p)

@app.route(APP_ROOT + '/mailto/<receiver>')
def view_mail_daily_products(receiver):
    products = view.ProductHuntDB().read_top_vote_products(days = 2, maxnum = 50)
    _log("mailto: %s" % (receiver))
    return mail_products(None, products, receiver)

def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

def user_event_day_top_voted(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'DAY_TOP_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '1' \
            or msg['Content'].lower() == 'dtv' \
            or msg['Content'].lower() == 'day_top_voted')
    return isclick or iscmd

def user_event_week_top_voted(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'WEEK_TOP_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '2' \
            or msg['Content'].lower() == 'wtv' \
            or msg['Content'].lower() == 'week_top_voted')
    return isclick or iscmd

def user_event_month_top_voted(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'MONTH_TOP_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '3' \
            or msg['Content'].lower() == 'mtv' \
            or msg['Content'].lower() == 'month_top_voted')
    return isclick or iscmd

def user_event_day_top_comments(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'DAY_TOP_COMMENTS'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '4' \
            or msg['Content'].lower() == 'dtc' \
            or msg['Content'].lower() == 'day_top_comments')
    return isclick or iscmd

def user_event_week_top_comments(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'WEEK_TOP_COMMENTS'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '5' \
            or msg['Content'].lower() == 'wtc' \
            or msg['Content'].lower() == 'week_top_comments')
    return isclick or iscmd

def user_event_month_top_comments(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'MONTH_TOP_COMMENTS'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '6' \
            or msg['Content'].lower() == 'mtc' \
            or msg['Content'].lower() == 'month_top_comments')
    return isclick or iscmd

def user_event_day_top_cv(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'DAY_TOP_COMMENT_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '7' \
            or msg['Content'].lower() == 'dtcv' \
            or msg['Content'].lower() == 'day_top_comment_voted')
    return isclick or iscmd

def user_event_week_top_cv(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'WEEK_TOP_COMMENT_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '8' \
            or msg['Content'].lower() == 'wtcv' \
            or msg['Content'].lower() == 'week_top_comment_voted')
    return isclick or iscmd

def user_event_month_top_cv(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'MONTH_TOP_COMMENT_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '9' \
            or msg['Content'].lower() == 'mtcv' \
            or msg['Content'].lower() == 'month_top_comment_voted')
    return isclick or iscmd

def user_event_search(msg):
    iscmd = msg['MsgType'] == 'text' and msg['Content'].startswith("search:")
    return iscmd

def user_event_mail(msg):
    iscmd = msg['MsgType'] == 'text' and msg['Content'].startswith("mail:")
    return iscmd

def user_event_unknow(msg):
    return True

def push_welcome_info(msg):
    return response_text_msg(msg, WELCOME_INFO + HELP_INFO)

def push_help_info(msg):
    return response_text_msg(msg, HELP_INFO)

def push_products(msg, products):
    _log("push_products: %d products" % (len(products)))
    if products is not None and len(products) > 0:
        return response_products_msg(msg, products)
    else:
        return

def mail_products(msg, products, receiver):
    """ Generate weixin href text and send to receiver """
    info = "Mail sent to " + receiver
    if products is not None and len(products) > 0:
        body = ""
        for p in products:
            item = WX_TEXT_TPL % (p.name, p.url, p.description)
            body += item
        try:
            _send_mail(receiver, body)
        except:
            info = "Failed to send mail to " + receiver
    else:
        info = ERROR_INFO

    if msg is not None:
        return response_text_msg(msg, info)
    else:
        return info + "\n"

def _send_mail(receiver, body):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender = 'sfox.studio@qq.com'
    subject = 'PH - ' + time.strftime("%Y%m%d")
    smtpserver = 'smtp.qq.com'
    username = 'sfox.studio@qq.com'
    password = 'XXxx1234'

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject

    # attachment
    att = MIMEText(body, 'base64', 'utf-8')
    att["Content-Type"] = 'text/plain'
    att["Content-Disposition"] = 'attachment; filename="%s.txt"' % (time.strftime("%Y%m%d"))
    msgRoot.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

def push_day_top_voted_products(msg):
    products = view.ProductHuntDB().read_top_vote_products(days = 2, maxnum = 10)
    return push_products(msg, products)

def push_week_top_voted_products(msg):
    products = view.ProductHuntDB().read_top_vote_products(days = 7, maxnum = 10)
    return push_products(msg, products)

def push_month_top_voted_products(msg):
    products = view.ProductHuntDB().read_top_vote_products(days = 30, maxnum = 10)
    return push_products(msg, products)

def push_day_top_comments_products(msg):
    products = view.ProductHuntDB().read_top_comments_products(days = 2, maxnum = 10)
    return push_products(msg, products)

def push_week_top_comments_products(msg):
    products = view.ProductHuntDB().read_top_comments_products(days = 7, maxnum = 10)
    return push_products(msg, products)

def push_month_top_comments_products(msg):
    products = view.ProductHuntDB().read_top_comments_products(days = 30, maxnum = 10)
    return push_products(msg, products)

def push_day_top_cv_products(msg):
    products = view.ProductHuntDB().read_top_cv_products(days = 2, maxnum = 10)
    return push_products(msg, products)

def push_week_top_cv_products(msg):
    products = view.ProductHuntDB().read_top_cv_products(days = 7, maxnum = 10)
    return push_products(msg, products)

def push_month_top_cv_products(msg):
    products = view.ProductHuntDB().read_top_cv_products(days = 30, maxnum = 10)
    return push_products(msg, products)

def push_search_result_products(msg):
    # skip prefix 'search:'
    keyword = msg['Content'][7:]
    products = view.ProductHuntDB().search_products(keyword)
    _log("search_products: %s" % (keyword))
    return push_products(msg, products)

def mail_day_top_voted_products(msg):
    # skip prefix 'mail:'
    receiver = msg['Content'][5:]
    products = view.ProductHuntDB().read_top_vote_products(days = 2, maxnum = 30)
    _log("mailto: %s" % (receiver))
    return mail_products(msg, products, receiver)

# weixin event handlers
_event_procs = [
    (user_subscribe_event, push_welcome_info),
    (user_event_day_top_voted, push_day_top_voted_products),
    (user_event_week_top_voted, push_week_top_voted_products),
    (user_event_month_top_voted, push_month_top_voted_products),
    (user_event_day_top_comments, push_day_top_comments_products),
    (user_event_week_top_comments, push_week_top_comments_products),
    (user_event_month_top_comments, push_month_top_comments_products),
    (user_event_day_top_cv, push_day_top_cv_products),
    (user_event_week_top_cv, push_week_top_cv_products),
    (user_event_month_top_cv, push_month_top_cv_products),
    (user_event_search, push_search_result_products),
    (user_event_mail, mail_day_top_voted_products),
    (user_event_unknow, push_help_info)
]

# view product comments
@app.route(APP_ROOT + '/producthunt/<guid>', methods=['GET'])
def view_product_comments(guid):
    p = view.ProductHuntDB().read_product(guid)
    if p is not None:
        _log("view_product_comments: postid=%s" % (p.postid))
        return render_template('comments.jinja.html', product=p)
    else:
        return ERROR_INFO

# verify for weixin server.
# weixin server will send GET request first to verify this backend
@app.route(APP_ROOT + '/weixin', methods=['GET'])
def weixin_access_verify():
    echostr = request.args.get('echostr')
    if verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'

# reciever msgs from weixin server
@app.route(APP_ROOT + '/weixin', methods=['POST'])
def weixin_msg():
    if verification(request):
        data = request.data
        msg = parse_msg(data)
        _log(msg)
        for (event, handler) in _event_procs:
            if event(msg):
                return handler(msg)
    return 'message processing fail'

# verify the weixin server
def verification(req):
    signature = req.args.get('signature')
    timestamp = req.args.get('timestamp')
    nonce = req.args.get('nonce')

    if signature is None or timestamp is None or nonce is None:
        return False

    token = APP_TOKEN
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True
    return False

def parse_msg(rawmsgstr):
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'],
        str(int(time.time())), content)
    return s

def response_products_msg(msg, products):
    s = ARTICLES_MSG_TPL_HEAD % (msg['FromUserName'], msg['ToUserName'],
        str(int(time.time())), len(products))
    for p in products:
        url = "http://www.producthunt.com/posts/" + p.postid

        if p == products[0]:
            tagline = '[%s] %s' % (p.postdate, p.description)
            if hasattr(p, 'sum_cv'):
                title = '[%dCV %dV %dC] [%s] %s - %s' % (p.sum_cv, p.vote_count, \
                    p.comment_count, p.postdate, p.name, p.description)
            else:
                title = '[%dV %dC] [%s] %s - %s' % (p.vote_count, \
                    p.comment_count, p.postdate, p.name, p.description)
            picUrl = APP_HOST + "/static/img/producthunt.png"
            item = ARTICLES_ITEM_TPL % (title, tagline, picUrl, url)
        else:
            tagline = '[%s] %s' % (p.postdate, p.description)
            if hasattr(p, 'sum_cv'):
                title = '[%dCV %dV %dC] %s\r\n%s' % (p.sum_cv, p.vote_count, \
                    p.comment_count, p.name, tagline)
            else:
                title = '[%dV %dC] %s\r\n%s' % (p.vote_count, p.comment_count, \
                    p.name, tagline)
            item = ARTICLES_ITEM_TPL % (title, tagline, p.user.icon, url)
        s = s + item
    s = s + ARTICLES_MSG_TPL_TAIL
    return s

def _log(msg):
    if APP_DEBUG:
        print msg

if __name__ == '__main__':
    app.run()
