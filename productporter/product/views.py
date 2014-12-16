#!/bin/env python
# -*- coding: utf-8 -*-
"""
    productporter.product.views
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    product blueprint

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import datetime
import json
from flask import Blueprint, request, current_app, flash, redirect, url_for, jsonify

from productporter.product.phapi import ProductHuntAPI
from productporter.product.models import Product
from productporter.utils import render_template, pull_and_save_posts
from productporter.utils import render_markup, query_products

product = Blueprint('product', __name__)

def _post_aquire_translate(request):
    """aquire to translate post"""
    postid = request.args.get('postid')
    post = Product.query.filter(Product.postid==postid).first_or_404()
    ret = {
        'status': 'success',
        'ctagline': post.ctagline
    }
    return jsonify(**ret)

# post detail
@product.route('/post', methods=["GET", "PUT"])
def post():
    if request.method == 'GET':
        return _post_aquire_translate(request)

    postid = request.args.get('postid')
    jsondata = json.loads(request.data)
    if not postid:
        postid = jsondata['postid']
    ctagline = jsondata['ctagline']
    post = Product.query.filter(Product.postid==postid).first_or_404()
    post.ctagline = ctagline
    post.save()
    ret = {
        'status': 'success',
        'ctagline': render_markup(post.ctagline)
        }
    return jsonify(**ret)

# posts list
@product.route('/posts', methods=["GET"])
def posts():
    """ product posts home dashboard """
    spec_day = request.args.get('day', '')
    day, posts = query_products(spec_day)
    post_count = len(posts)

    return render_template('product/posts.jinja.html',
        post_count=post_count, posts=posts, day=day)

#homepage just for fun
@product.route('/pull')
def pull():
    """ pull data from producthunt.com """
    day = request.args.get('day', '')
    count = pull_and_save_posts(day)
    return "pulled %d posts " % (count)

