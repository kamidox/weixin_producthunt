#!/bin/env python
# -*- coding: utf-8 -*-
"""
    productporter.weixin.view
    ~~~~~~~~~~~~~~~~~

    weixin backend blueprint

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import hashlib, time
import xml.etree.ElementTree as ET

from flask import Blueprint, request, current_app, redirect, url_for

from productporter.weixin.consts import *
from productporter.utils.helper import query_products, format_date, \
    query_top_voted_products, query_search_products, send_mail

weixin = Blueprint('weixin', __name__)

#homepage just for fun
@weixin.route('/')
def index():
    """ weixin backend home """
    return redirect(url_for('product.posts'))

@weixin.route('/mailto/<receiver>')
def view_mail_daily_products(receiver):
    """ mail products to receiver """
    day, products = query_products()
    current_app.logger.info("mailto %s of %s products in %s" % \
        (receiver, len(products), day))
    return mail_products(None, products, receiver)

def user_subscribe_event(msg):
    """ user subscribe event """
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

def user_event_day_top_voted(msg):
    """ day top voted """
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'DAY_TOP_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '1' \
            or msg['Content'].lower() == 'dtv' \
            or msg['Content'].lower() == 'day_top_voted')
    return isclick or iscmd

def user_event_week_top_voted(msg):
    """ week top voted """
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'WEEK_TOP_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '2' \
            or msg['Content'].lower() == 'wtv' \
            or msg['Content'].lower() == 'week_top_voted')
    return isclick or iscmd

def user_event_month_top_voted(msg):
    """ month top voted """
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'MONTH_TOP_VOTED'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == '3' \
            or msg['Content'].lower() == 'mtv' \
            or msg['Content'].lower() == 'month_top_voted')
    return isclick or iscmd

def user_event_search(msg):
    """ search product """
    iscmd = msg['MsgType'] == 'text' and msg['Content'].startswith("search:")
    return iscmd

def user_event_mail(msg):
    """ mail products """
    iscmd = msg['MsgType'] == 'text' and msg['Content'].startswith("mail:")
    return iscmd

def user_event_help(msg):
    """ help event """
    isclick = msg['MsgType'] == 'event' \
        and msg['Event'] == 'CLICK' and msg['EventKey'] == 'HELP'
    iscmd = msg['MsgType'] == 'text' and \
        (msg['Content'].lower() == 'h' \
            or msg['Content'].lower() == 'help')
    return isclick or iscmd

def user_event_feedback(msg):
    """ last unknow event """
    return True

def push_welcome_info(msg):
    """ push welcome info """
    return response_text_msg(msg, WELCOME_INFO + HELP_INFO)

def push_help_info(msg):
    """ push help info """
    return response_text_msg(msg, HELP_INFO)

def push_thanks_info(msg):
    """ push thanks info """
    return response_text_msg(msg, THANKS_INFO)

def push_products(msg, products):
    """ push products """
    current_app.logger.info("push_products: %d products" % (len(products)))
    if products is not None and len(products) > 0:
        return response_products_msg(msg, products)
    else:
        return response_text_msg(msg, ERROR_INFO)

def mail_products(msg, products, receiver):
    """ Generate weixin href text and send to receiver """
    info = "Mail sent to " + receiver
    if products is not None and len(products) > 0:
        body = ""
        for prod in products:
            item = WX_TEXT_TPL % (prod.name, prod.redirect_url, prod.tagline)
            body += item
        try:
            send_mail(
                subject='PH - ' + time.strftime("%Y%m%d"),
                recipient=receiver,
                body=body,
                subtype="html",
                as_attachment=True)
        except:
            info = "Failed to send mail to " + receiver
    else:
        info = ERROR_INFO

    if msg is not None:
        return response_text_msg(msg, info)
    else:
        return info + "\n"

def push_day_top_voted_products(msg):
    """ push day top voted """
    products = query_top_voted_products(days_ago=2, limit=10)
    return push_products(msg, products)

def push_week_top_voted_products(msg):
    """ push week top voted """
    products = query_top_voted_products(days_ago=7, limit=10)
    return push_products(msg, products)

def push_month_top_voted_products(msg):
    """ push month top voted """
    products = query_top_voted_products(days_ago=30, limit=10)
    return push_products(msg, products)

def push_search_result_products(msg):
    """ push search result """
    # skip prefix 'search:'
    keyword = msg['Content'][7:]
    products = query_search_products(keyword)
    current_app.logger.info("search_products: %s" % (keyword))
    return push_products(msg, products)

def mail_day_top_voted_products(msg):
    """ mail day top voted products """
    # skip prefix 'mail:'
    receiver = msg['Content'][5:]
    products = query_top_voted_products(days_ago=2, limit=50)
    current_app.logger.info("mailto: %s" % (receiver))
    return mail_products(msg, products, receiver)

# weixin event handlers
EVENT_PROCS = [
    (user_subscribe_event, push_welcome_info),
    (user_event_day_top_voted, push_day_top_voted_products),
    (user_event_week_top_voted, push_week_top_voted_products),
    (user_event_month_top_voted, push_month_top_voted_products),
    (user_event_search, push_search_result_products),
    (user_event_mail, mail_day_top_voted_products),
    (user_event_help, push_help_info),
    (user_event_feedback, push_thanks_info),
]

# verify for weixin server.
# weixin server will send GET request first to verify this backend
@weixin.route('/weixin', methods=['GET'])
def weixin_access_verify():
    """ weixin access verify """
    print("weixin_access_verify")
    echostr = request.args.get('echostr')
    if verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'

# reciever msgs from weixin server
@weixin.route('/weixin', methods=['POST'])
def weixin_msg():
    """ weixin access verify """
    if verification(request):
        data = request.data
        msg = parse_msg(data)
        for (event, handler) in EVENT_PROCS:
            if event(msg):
                return handler(msg)
    return 'message processing fail'

def verification(req):
    """verify the weixin server"""
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
    """ parse message """
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def response_text_msg(msg, content):
    """ response text message """
    result = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'],
        str(int(time.time())), content)
    return result

def response_products_msg(msg, products):
    """ response xml message """
    result = ARTICLES_MSG_TPL_HEAD % (msg['FromUserName'], msg['ToUserName'],
        str(int(time.time())), len(products))
    for prod in products:
        tagline = '[%s] %s' % (format_date(prod.date), prod.tagline)
        if prod == products[0]:
            title = '[%dV] [%s] %s - %s' % (prod.votes_count, prod.date, \
                prod.name, prod.tagline)
        else:
            title = '[%dV] %s\r\n%s' % (prod.votes_count, prod.name, tagline)

        item = ARTICLES_ITEM_TPL % (title, tagline, prod.screenshot_url, \
            prod.redirect_url)
        result = result + item
    result = result + ARTICLES_MSG_TPL_TAIL
    return result
