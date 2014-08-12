#!/bin/env python
# -*- coding: utf-8 -*-
import hashlib, urllib, urllib2, re, time, json
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template, send_from_directory
from private_const import *

app = Flask(__name__)
app.debug = True
app.secret_key = APP_SECRET_KEY

#homepage just for fun
@app.route('/')
def home():
    return render_template('index.html')

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
        if user_subscribe_event(msg):
            return help_info(msg)
        else:
            return help_info_cute(msg)
    return 'message processing fail'

# verify the weixin server
def verification(request):
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

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

def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

def help_info(msg):
    return response_text_msg(msg, HELP_INFO)

def help_info_cute(msg):
    return response_text_msg(msg, HELP_INFO_CUTE)

def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'],
        str(int(time.time())), content)
    return s

def _log(msg):
    if app.debug:
        print msg

if __name__ == '__main__':
    app.run()
