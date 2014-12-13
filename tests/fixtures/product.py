# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import pytest
from productporter.product.phapi import ProductHuntAPI

@pytest.fixture(scope="session")
def posts():
    """
    Pull posts from producthunt.com with offical API
    """
    api = ProductHuntAPI()
    return api.posts()

@pytest.fixture(scope="session")
def old_posts(old_day):
    """
    Pull posts from producthunt.com with offical API
    """
    api = ProductHuntAPI()
    return api.posts(old_day)

@pytest.fixture(scope="session")
def old_day():
    """Return some old day of date"""
    return '2014-12-02'
