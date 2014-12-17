# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import re
from productporter.product.phapi import ProductHuntAPI
from productporter.product.models import Product

def test_sample_posts_not_empty(some_posts):
    """
    Test some posts not empty
    """
    assert len(some_posts) > 0

def test_sample_posts_in_db(database, some_posts):
    """
    Save some posts to database
    """
    for jsondata in some_posts:
        pi = Product.query.filter(Product.postid==jsondata['id']).first()
        assert pi is None
        pi = Product.from_json(jsondata)
        pi.save()

    assert Product.query.count() == len(some_posts)
