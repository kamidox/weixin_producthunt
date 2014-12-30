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
from productporter.utils.helper import render_template, pull_and_save_posts, render_markup, \
    query_products, can_translate, can_review, is_online
from productporter.utils.decorators import moderator_required
from productporter.user.models import User

product = Blueprint('product', __name__)

def _render_contributors(contributers, postid):
    """render contributors, refer to macro 'contributors' in macro.jinja.html"""
    div_template = "<div class='translaters-list' data-postid='%s'> by %s</div>"
    user_template = "<a href='%s'>@%s</a>"
    user_htmls = []
    users = contributers.all()
    for user in users:
        nickname = user.nickname if user.nickname else user.username
        user_htmls.append(user_template % \
            (url_for('user.profile', username=user.username), nickname))
    return div_template % (postid, '\n'.join(user_htmls))

def _post_aquire_translate(request):
    """aquire to translate post"""
    postid = request.args.get('postid')
    field = request.args.get('field', 'ctagline')

    current_app.logger.info('aquire translate %s for post %s' % (field, str(postid)))
    if not can_translate(current_user):
        ret = {
            'status': 'error',
            'postid': postid,
            'error': 'Please sign in first'
            }
        return make_response(jsonify(**ret), 401)

    post = Product.query.filter(Product.postid==postid).first_or_404()
    if getattr(post, field + '_locked'):
        ret = {
            'status': 'error',
            'postid': postid,
            'error': '%s is locked. Please contact adminitrator.'
            }
        return make_response(jsonify(**ret), 403)

    editing_user = getattr(post, 'editing_' + field + '_user')
    if (editing_user) and \
        (editing_user.username != current_user.username) and \
        (is_online(editing_user)):
        ret = {
            'status': 'error',
            'postid': post.postid,
            'error': '%s is editing by %s' % \
                (field, editing_user.username)
            }
        return make_response(jsonify(**ret), 400)

    setattr(post, 'editing_' + field + '_user_id', current_user.id)
    post.save()
    ret = {
            'status': 'success',
            'postid': post.postid,
            'field': field,
            'value': getattr(post, field)
        }
    return jsonify(**ret)

# translate detail
@product.route('/translate', methods=["GET", "PUT", "POST"])
def translate():
    """
    use GET to aquire translation
    use PUT/POST to commit translation

    :param postid: The postid of product
    :param field: The field of operation, could be 'ctagline' or 'cintro'
    :param value: The value of translate field
    """
    if request.method == 'GET':
        return _post_aquire_translate(request)

    jsondata = None
    try:
        jsondata = json.loads(request.data)
    except ValueError:
        ret = {
            'status': 'error',
            'message': "invalid json data"
        }
        return make_response(jsonify(**ret), 405)

    postid = jsondata['postid']
    field = jsondata['field']

    if not can_translate(current_user):
        ret = {
            'status': 'error',
            'postid': postid,
            'field': field,
            'error': 'Please sign in first'
            }
        return make_response(jsonify(**ret), 401)

    post = Product.query.filter(Product.postid==postid).first_or_404()

    try:
        canceled = jsondata['canceled']
        if canceled:
            setattr(post, 'editing_' + field + '_user_id', None)
            post.save()
            ret = {
                'status': 'success',
                'postid': post.postid,
                'field': field
                }
            return jsonify(**ret)
    except KeyError:
        pass

    current_app.logger.info('commit %s for post %s' % (field, str(postid)))

    setattr(post, field, jsondata['value'])
    setattr(post, 'editing_' + field + '_user_id', None)
    post.save()
    getattr(current_user, 'add_' + field + '_product')(post)
    ret = {
        'status': 'success',
        'postid': post.postid,
        'field': field,
        'value': render_markup(getattr(post, field)),
        'contributors': _render_contributors( \
            getattr(post, field + '_editors'), post.postid)
    }

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

#pull products
@product.route('/pull')
def pull():
    """ pull data from producthunt.com """
    day = request.args.get('day', '')
    count = pull_and_save_posts(day)
    return "pulled %d posts " % (count)

def _render_translate_button(post, op):
    """render translate button"""
    if op.lower() == 'lock':
        template = '<button name="translate" type="button" class="btn btn-primary" \
                    data-postid="%s" \
                    data-url="%s">Translate</button>'
        return template % (post.postid, url_for('product.translate'))
    return ''

def _render_lock_button(post, op):
    """render lock button"""
    param = {'postid': post.postid,
        'op': op,
        'url': url_for('product.lock'),
    }
    template = '<button name="lock" type="button" class="btn btn-primary" \
                data-postid="%(postid)s" op="%(op)s" \
                data-url="%(url)s">%(op)s</button>'
    return template % param

@product.route('/lock', methods=['GET'])
@moderator_required
def lock():
    """
    lock product

    :param postid: The postid of product
    :param op: Operation, clould be 'lock' or 'unlock'
    :param field: Field, could be 'ctagline' or 'cintro'
    """
    postid = request.args.get('postid', '')
    op = request.args.get('op', 'lock')
    field = request.args.get('field', 'ctagline')
    post = Product.query.filter(Product.postid==postid).first_or_404()

    fieldname = field + '_locked'
    if op.lower() == 'lock':
        setattr(post, fieldname, True)
        op = 'Unlock'
    else:
        setattr(post, fieldname, False)
        op = 'Lock'
    post.save()
    ret = {
        'status': 'success',
        'postid': post.postid,
        'translate': _render_translate_button(post, op),
        'lock': _render_lock_button(post, op),
    }
    return jsonify(**ret)


