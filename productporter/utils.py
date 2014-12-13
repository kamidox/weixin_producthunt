# -*- coding: utf-8 -*-
"""
    productporter.utils.populate
    ~~~~~~~~~~~~~~~~~~~~

    A module that makes creating data more easily

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
from productporter.user.models import User, Group
from productporter.product.phapi import ProductHuntAPI
from productporter.product.models import Product

def create_default_groups():
    """
    This will create the 5 default groups
    """
    from productporter.fixtures.groups import fixture
    result = []
    for key, value in fixture.items():
        group = Group(name=key)

        for k, v in value.items():
            setattr(group, k, v)

        group.save()
        result.append(group)
    return result

def create_admin_user(username, password, email):
    """
    Creates the administrator user
    """
    admin_group = Group.query.filter_by(admin=True).first()
    user = User()

    user.username = username
    user.password = password
    user.email = email
    user.primary_group_id = admin_group.id

    user.save()

def pull_and_save_posts(day=None):
    """
    Pull and save posts to database
    """
    api = ProductHuntAPI()
    posts = api.posts(day)
    for jsondata in posts:
        pi = Product()
        pi.from_json(jsondata)
        pi.save()

