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

def test_user_and_groups(user, moderator_user, admin_user):
    """test user and group and it's permission"""
    assert user.username == 'test_normal'
    assert user.email == 'test_normal@example.org'
    assert user.password != 'test'
    assert user.check_password('test') == True

    assert moderator_user.username == 'test_mod'
    assert moderator_user.email == 'test_mod@example.org'
    assert moderator_user.password != 'test'
    assert moderator_user.check_password('test') == True

    assert admin_user.username == 'test_admin'
    assert admin_user.email == 'test_admin@example.org'
    assert admin_user.password != 'test'
    assert admin_user.check_password('test') == True

    perms = user.permissions
    assert perms['admin'] == False
    assert perms['mod'] == False
    assert perms['member'] == True
    assert perms['guest'] == False
    assert perms['perm_translate'] == True
    assert perms['perm_comment'] == True
    assert perms['perm_review'] == True
    assert perms['perm_report'] == False
    assert perms['perm_topic'] == False
    assert perms['perm_setgroup'] == False

    user.add_to_group(moderator_user.primary_group)
    perms = user.permissions
    assert user.in_group(moderator_user.primary_group) == True
    assert perms['admin'] == False
    assert perms['mod'] == True
    assert perms['member'] == True
    assert perms['guest'] == False
    assert perms['perm_translate'] == True
    assert perms['perm_comment'] == True
    assert perms['perm_review'] == True
    assert perms['perm_report'] == True
    assert perms['perm_topic'] == True
    assert perms['perm_setgroup'] == False

    user.add_to_group(admin_user.primary_group)
    perms = user.permissions
    assert user.in_group(admin_user.primary_group) == True
    assert perms['admin'] == True
    assert perms['mod'] == True
    assert perms['member'] == True
    assert perms['guest'] == False
    assert perms['perm_translate'] == True
    assert perms['perm_comment'] == True
    assert perms['perm_review'] == True
    assert perms['perm_report'] == True
    assert perms['perm_topic'] == True
    assert perms['perm_setgroup'] == True
