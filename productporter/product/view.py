#!/bin/env python
# -*- coding: utf-8 -*-
"""
    productporter.product.view
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    product blueprint

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import datetime
from flask import Blueprint, request, render_template, current_app

from productporter.product.phapi import ProductHuntAPI
from productporter.product.models import Product

products = Blueprint('products', __name__)

#homepage just for fun
@products.route('/')
def home():
    """ product home dashboard"""
    day = request.args.get('day', '')
    if not day:
        d = datetime.date.today()
        day = '%d-%d-%d' % (d.year, d.month, d.day)
    posts = Product.query.filter(Product.date==day).all()
    return render_template('posts.jinja.html',
        post_count=len(posts), posts=posts, date=day)

#homepage just for fun
@products.route('/pull')
def pull():
    """ pull data from producthunt.com """
    api = ProductHuntAPI()
    day = request.args.get('day', '')
    api.posts(day)

