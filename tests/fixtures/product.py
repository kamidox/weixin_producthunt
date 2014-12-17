# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import pytest
import json
from productporter.product.phapi import ProductHuntAPI
from productporter.product.models import Product
# Use the development configuration if available
try:
    from productporter.configs.development import DevelopmentConfig as Config
except ImportError:
    from productporter.configs.default import DefaultConfig as Config

@pytest.fixture(scope="session")
def some_day():
    """Return some old day of date"""
    return '2014-12-16'

@pytest.fixture(scope="session")
def some_posts(some_day):
    """
    Pull posts from producthunt.com with offical API
    """
    if Config.PH_API_USE_LOCAL_SAMPLE_DATA:
        from sampledata import SAMPLE_DATA
        jsondata = json.loads(SAMPLE_DATA)
        return jsondata['posts']
    else:
        api = ProductHuntAPI()
        return api.posts(some_day)

@pytest.fixture()
def db_posts(database, some_posts):
    """
    Pull posts from producthunt.com with offical API
    And save to database as sample test data
    """
    postids=[]
    for jsondata in some_posts:
        pi = Product.query.filter(Product.postid==jsondata['id']).first()
        assert pi is None
        pi = Product.from_json(jsondata)
        pi.save()
        postids.append(pi.postid)

    return postids

