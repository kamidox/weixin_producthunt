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
from flask import Blueprint, request, current_app, flash, redirect, url_for

from productporter.product.phapi import ProductHuntAPI
from productporter.product.models import Product
from productporter.utils import render_template, pull_and_save_posts
from productporter.product.forms import TranslateForm

product = Blueprint('product', __name__)

#homepage just for fun
@product.route('/posts', methods=["GET", "POST"])
def posts():
    """ product posts home dashboard """
    edit_postid = request.args.get('edit_postid', '')
    spec_day = request.args.get('day', '')
    day = spec_day
    if not day:
        d = datetime.date.today()
        day = '%d-%d-%d' % (d.year, d.month, d.day)
    posts = Product.query.filter(Product.date==day).\
        order_by(Product.votes_count.desc()).all()
    post_count = len(posts)

    # when not specific a day and the content is empty, we show yesterday's data
    if not spec_day and post_count == 0:
        delta = datetime.timedelta(days=-1)
        d = datetime.date.today() + delta
        day = '%d-%d-%d' % (d.year, d.month, d.day)
    posts = Product.query.filter(Product.date==day).\
        order_by(Product.votes_count.desc()).all()
    post_count = len(posts)

    form = TranslateForm(request.form)
    if form.validate_on_submit():
        form.save()
        flash(("Translation saved"), "success")
        return redirect(url_for("product.posts", day=day))

    if edit_postid:
        for p in posts:
            if p.postid == edit_postid:
                form.ctagline.data = p.ctagline
                form.postid.data = p.postid
    return render_template('product/posts.jinja.html',
        post_count=post_count, posts=posts, day=day, edit_postid=edit_postid, form=form)

#homepage just for fun
@product.route('/pull')
def pull():
    """ pull data from producthunt.com """
    day = request.args.get('day', '')
    count = pull_and_save_posts(day)
    return "pulled %d posts " % (count)

