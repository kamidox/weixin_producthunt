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

def test_old_posts(old_posts):
    """
    Test old posts not empty
    """
    assert len(old_posts) > 0

def test_posts_not_empty(posts):
    """
    Test posts not empty
    """
    assert len(posts) >= 0

def test_save_posts(database, posts):
    """
    Save posts to database
    """
    for jsondata in posts:
        pi = Product.query.filter(Product.postid==jsondata['id']).first()
        assert pi is None
        pi = Product()
        pi.from_json(jsondata)
        pi.save()

    assert Product.query.count() == len(posts)
