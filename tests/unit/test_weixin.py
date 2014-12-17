# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""

import time
import random

def test_weixin_verification(app, test_client, server_url, weixin_signature):
    """weixin signature verify"""

    if not app.config['WEIXIN_UNITTEST']:
        return

    param = {'signature': weixin_signature[0],
        'timestamp': weixin_signature[1],
        'nonce': weixin_signature[2],
        'echostr': 'access ok'
    }
    r = test_client.get(server_url + '/weixin/weixin', query_string=param)
    assert r.status_code == 200
    assert r.data == 'access ok'

def test_weixin_send_msg(app, test_client, server_url, weixin_signature, db_posts):
    """send msg to weixin backend"""
    if not app.config['WEIXIN_UNITTEST']:
        return

    TPL_TEXT = '''
        <xml>
            <ToUserName><![CDATA[%(to)s]]></ToUserName>
            <FromUserName><![CDATA[%(from)s]]></FromUserName>
            <CreateTime>%(time)d</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%(content)s]]></Content>
            <MsgId>$(id)s</MsgId>
        </xml>
        '''

    param = {'signature': weixin_signature[0],
        'timestamp': weixin_signature[1],
        'nonce': weixin_signature[2]}

    msg = {"to": "ToUserName",
        "from": "FromUserName",
        "time": weixin_signature[3],
        "content": '1',
        "id": str(random.random())[-10:]}

    r = test_client.post(server_url + '/weixin/weixin', \
        data = TPL_TEXT % msg, query_string=param)
    assert r.status_code == 200
    print(r.data)



