# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import pytest

import time
import random
import hashlib
# Use the development configuration if available
try:
    from productporter.configs.development import DevelopmentConfig as Config
except ImportError:
    from productporter.configs.default import DefaultConfig as Config

@pytest.fixture()
def weixin_signature():
    t = time.time()
    timestamp = str(t)

    # I don't know how Weixin generate the 9-digit nonce, so I turn to random.
    nonce = str(int(random.random()))[-9:]

    l = [timestamp, nonce, Config.WEIXIN_TOKEN]
    l.sort()
    signature = hashlib.sha1("".join(l)).hexdigest()

    return signature, timestamp, nonce, t
