# -*- coding: utf-8 -*-
"""
    productporter.user.models
    ~~~~~~~~~~~~~~~~~~~~

    This module provides the models for the user.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""

import json
import requests
import time
from flask import current_app

class ProductHuntAPI(object):
    """Wrapper for producthunt api"""

    SCHEMA = "https://"
    HOST = 'api.producthunt.com'
    URL_CLIENT_AUTH = '/v1/oauth/token'
    URL_POSTS = '/v1/posts'
    HEADER = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Host': 'api.producthunt.com'
    }

    def __init__(self):
        """Create ProductHuntAPI"""
        super(ProductHuntAPI, self).__init__()
        self.access_token = None
        self.expires_in = 0

    def client_auth(self):
        """OAuth Client Only Authentication"""
        current_app.logger.info('start auth on %d' % (int(time.time())))
        data = {
            'client_id': current_app.config["PH_API_KEY"],
            'client_secret': current_app.config["PH_API_SECRET"],
            'grant_type': 'client_credentials'
        }
        url = self.SCHEMA + self.HOST + self.URL_CLIENT_AUTH
        r = requests.post(url, data=json.dumps(data), headers=self.HEADER)
        rsp = r.json()
        if r.status_code == 200:
            self.expires_in = int(time.time()) + int(rsp['expires_in']) - 1
            self.access_token = rsp['access_token']
        else:
            current_app.logger.error('auth failed. status_code=%d\n%s'
                % (r.status_code, json.dumps(rsp, sort_keys=True,
                    indent=4, separators=(',', ': '))))
            raise Exception(rsp['error'])

    def posts(self, day=None):
        """Get posts"""
        now = int(time.time())
        if self.access_token is None or self.expires_in < now:
            self.client_auth()

        current_app.logger.info('get posts on %s' % (day or "today"))
        params = None
        if day:
            params = {'day': day}
        url = self.SCHEMA + self.HOST + self.URL_POSTS
        headers = self.HEADER.copy()
        headers['Authorization'] = 'Bearer ' + self.access_token
        r = requests.get(url, headers=headers, params=params)
        rsp = r.json()
        if r.status_code == 200:
            return rsp['posts']
        else:
            # access token may expires unexpect, we try it one more time
            if r.status_code == 401:
                self.client_auth()
                r = requests.get(url, headers=headers)
                rsp = r.json()
                if r.status_code == 200:
                    return rsp['posts']

            current_app.logger.error('posts failed. status_code=%d\n%s'
                % (r.status_code, json.dumps(rsp, sort_keys=True,
                    indent=4, separators=(',', ': '))))
            raise Exception(rsp['error'])


