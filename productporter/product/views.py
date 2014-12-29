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
from flask import Blueprint, request, current_app, flash, redirect, \
    url_for, jsonify, make_response
from flask.ext.login import current_user

from productporter.product.phapi import ProductHuntAPI
from productporter.product.models import Product
from productporter.utils import render_template, pull_and_save_posts, render_markup, \
    query_products, can_translate, can_review, is_online

product = Blueprint('product', __name__)

def _render_contributors(contributers, postid):
    """render contributors, refer to macro 'contributors' in macro.jinja.html"""
    div_template = "<div class='translaters-list' data-postid='%s'> by %s</div>"
    user_template = "<a href='%s'>@%s</a>"
    user_htmls = []
    users = contributers.all()
    for user in users:
        user_htmls.append(user_template % \
            (url_for('user.profile', username=user.username), user.username))
    return div_template % (postid, '\n'.join(user_htmls))

def _post_aquire_translate(request):
    """aquire to translate post"""
    postid = request.args.get('postid')
    operate = request.args.get('operate')

    current_app.logger.info('aquire %s for post %s' % (operate, str(postid)))
    if not can_translate(current_user):
        ret = {
            'status': 'error',
            'postid': postid,
            'error': 'Please sign in first'
            }
        return make_response(jsonify(**ret), 401)

    post = Product.query.filter(Product.postid==postid).first_or_404()

    operating_user = None
    if operate == 'translate':
        operating_user = post.translating_user
    else:
        operating_user = post.introducing_user

    if (operating_user is not None) and \
            (operating_user.username != current_user.username) and \
            (is_online(operating_user)):
        ret = {
            'status': 'error',
            'postid': post.postid,
            'error': 'this product is in %s by %s' % \
                (operate, operating_user.username)
            }
        return make_response(jsonify(**ret), 400)

    if operate == 'translate':
        post.translating_user_id = current_user.id
        post.save()

        ret = {
            'status': 'success',
            'postid': post.postid,
            'ctagline': post.ctagline
        }
    else:
        post.introduing_user_id = current_user.id
        post.save()

        ret = {
            'status': 'success',
            'postid': post.postid,
            'cintro': post.cintro
        }
    return jsonify(**ret)

# translate detail
@product.route('/translate', methods=["GET", "PUT", "POST"])
def translate():
    """
    use GET to aquire translation
    use PUT/POST to commit translation

    return json data of product tagline
    """
    if request.method == 'GET':
        return _post_aquire_translate(request)

    postid = request.args.get('postid')
    operate = request.args.get('operate')
    jsondata = None
    try:
        jsondata = json.loads(request.data)
    except ValueError:
        ret = {
            'status': 'error',
            'message': "invalid json data"
        }
        return make_response(jsonify(**ret), 405)

    if not postid:
        postid = jsondata['postid']
    if not operate:
        operate = jsondata['operate']

    if not can_translate(current_user):
        ret = {
            'status': 'error',
            'postid': postid,
            'error': 'Please sign in first'
            }
        return make_response(jsonify(**ret), 401)

    post = Product.query.filter(Product.postid==postid).first_or_404()

    try:
        canceled = jsondata['canceled']
        if canceled:
            if operate == 'translate':
                post.translating_user_id = None
            else:
                post.introducing_user_id = None
            post.save()
            ret = {
                'status': 'success',
                'postid': post.postid,
                }
            return jsonify(**ret)
    except KeyError:
        pass

    current_app.logger.info('commit %s for post %s' % (operate, str(postid)))
    ret = {
        'status': 'success',
        'postid': post.postid,
    }

    if operate == 'translate':
        try:
            post.ctagline = jsondata['ctagline']
        except KeyError:
            post.ctagline = ""
        post.translating_user_id = None
        post.save()
        current_user.add_translated_product(post)
        ret.update({'ctagline': post.ctagline})
        ret.update({'contributors': _render_contributors( \
            post.translaters, post.postid)})
    else:
        try:
            post.cintro = jsondata['cintro']
        except KeyError:
            post.cintro = ""
        post.introducing_user_id = None
        post.save()
        current_user.add_introduced_product(post)
        ret.update({'cintro': render_markup(post.cintro)})
        ret.update({'contributors': _render_contributors( \
            post.introducers, post.postid)})

    return jsonify(**ret)

# posts list
@product.route('/', methods=["GET"])
def index():
    """ product posts home dashboard """
    return redirect(url_for('product.posts'))

# posts list
@product.route('/posts/', methods=["GET"])
def posts():
    """ product posts home dashboard """
    spec_day = request.args.get('day', '')
    day, posts = query_products(spec_day)
    post_count = len(posts)

    return render_template('product/posts.jinja.html',
        post_count=post_count, posts=posts, day=day)

# posts list
@product.route('/posts/<postid>', methods=["GET"])
def post_intro(postid):
    """ product detail information page """

    post = Product.query.filter(Product.postid==postid).first_or_404()
    return render_template('product/post_intro.jinja.html', post=post)

#homepage just for fun
@product.route('/pull')
def pull():
    """ pull data from producthunt.com """
    day = request.args.get('day', '')
    count = pull_and_save_posts(day)
    return "pulled %d posts " % (count)

