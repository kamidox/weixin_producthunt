# -*- coding: utf-8 -*-
"""
    productporter.utils.populate
    ~~~~~~~~~~~~~~~~~~~~

    A module that makes creating data more easily

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app
from flask.ext.themes2 import render_theme_template

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
        pi = Product.from_json(jsondata)
        pi.save()
    return len(posts)

def render_template(template, **context):
    """
    A helper function that uses the `render_theme_template` function
    without needing to edit all the views
    """
    theme = current_app.config['DEFAULT_THEME']
    return render_theme_template(theme, template, **context)

