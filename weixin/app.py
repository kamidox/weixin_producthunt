#!/bin/env python
# -*- coding: utf-8 -*-
import hashlib, time
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template
from private_const import *
import view

app = Flask(__name__)
app.debug = APP_DEBUG

#homepage just for fun
@app.route('/')
def home():
    return render_template('index.html')

#homepage just for fun
@app.route('/weixin_test')
def weixin_test():
    p = view.populate_test_data()
    return render_template('comments.jinja.html', product=p)

def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

def user_event_day_top(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'DAY_TOP'
    iscmd = msg['MsgType'] == 'text' and msg['Content'] == '1'
    return isclick or iscmd

def user_event_week_top(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'WEEK_TOP'
    iscmd = msg['MsgType'] == 'text' and msg['Content'] == '2'
    return isclick or iscmd

def user_event_month_top(msg):
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'MONTH_TOP'
    iscmd = msg['MsgType'] == 'text' and msg['Content'] == '3'
    return isclick or iscmd

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
        return response_text_msg(msg, ERROR_INFO)

def push_day_top_products(msg):
    products = view.ProductHuntDB().read_top_vote_products(days = 2, maxnum = 10)
    return push_products(msg, products)

def push_week_top_products(msg):
    products = view.ProductHuntDB().read_top_vote_products(days = 7, maxnum = 10)
    return push_products(msg, products)

def push_month_top_products(msg):
    products = view.ProductHuntDB().read_top_vote_products(days = 30, maxnum = 10)
    return push_products(msg, products)

# weixin event handlers
_event_procs = [
    (user_subscribe_event, push_welcome_info), # subscribe
    (user_event_day_top, push_day_top_products), #CLICK->DAY_TOP
    (user_event_week_top, push_week_top_products), #CLICK->WEEK_TOP
    (user_event_month_top, push_month_top_products), #CLICK->MONTH_TOP
    (user_event_unknow, push_help_info)
]

# view product comments
@app.route('/producthunt/<guid>', methods=['GET'])
def view_product_comments(guid):
    p = view.ProductHuntDB().read_product(guid)
    if p is not None:
        _log("view_product_comments: postid=%s" % (p.postid))
        return render_template('comments.jinja.html', product=p)
    else:
        return ERROR_INFO

# verify for weixin server.
# weixin server will send GET request first to verify this backend
@app.route('/weixin', methods=['GET'])
def weixin_access_verify():
    echostr = request.args.get('echostr')
    if verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'

# reciever msgs from weixin server
@app.route('/weixin', methods=['POST'])
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
        url = APP_HOST + "/producthunt/"+ p.guid
        tagline = '[%s] %s' % (p.postdate, p.description)
        title = '[%d] %s\r\n%s' % (p.vote_count, p.name, tagline)
        if p == products[0]:
            picUrl = APP_HOST + "/static/img/producthunt.png"
            item = ARTICLES_ITEM_TPL % (title, tagline, picUrl, url)
        else:
            item = ARTICLES_ITEM_TPL % (title, tagline, p.user.icon, url)
        s = s + item
    s = s + ARTICLES_MSG_TPL_TAIL
    return s

def _log(msg):
    if APP_DEBUG:
        print msg

if __name__ == '__main__':
    app.run()
