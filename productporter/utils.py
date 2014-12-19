# -*- coding: utf-8 -*-
"""
    productporter.utils.populate
    ~~~~~~~~~~~~~~~~~~~~

    A module that makes creating data more easily

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import datetime
from markdown2 import markdown as render_markdown

from flask import current_app
from flask.ext.themes2 import render_theme_template
from flask import render_template as flask_render_template

from productporter.extensions import db
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

def render_markup(text):
    """Renders the given text as markdown

    :param text: The text to be rendered
    """
    return render_markdown(text, extras=['tables'])

def query_products(spec_day=None):
    """ get all the products of the day """
    day = spec_day
    if not day:
        day = date_format(datetime.date.today())
    posts = Product.query.filter(Product.date==day).\
        order_by(Product.votes_count.desc()).all()

    # when not specific a day and the content is empty, we show yesterday's data
    if not spec_day and len(posts) == 0:
        delta = datetime.timedelta(days=-1)
        d = datetime.date.today() + delta
        day = date_format(d)
    posts = Product.query.filter(Product.date==day).\
        order_by(Product.votes_count.desc()).all()

    return day, posts

def query_top_voted_products(days_ago=2, limit=10):
    """ query to voted products days ago """
    delta = datetime.timedelta(days=-days_ago)
    d2 = datetime.date.today()
    d1 = d2 + delta
    return Product.query.filter(Product.date.between(d1, d2)).\
        order_by(Product.votes_count.desc()).limit(limit).offset(0).all()

def query_search_products(keyword, limit=10):
    """ search product in product's name and tagline """
    k = '%%%s%%' % (keyword)
    return Product.query.filter(db.or_(Product.name.like(k), \
        Product.tagline.like(k))).order_by(Product.votes_count.desc()).\
        limit(limit).offset(0).all()

def date_format(d):
    """ format a datetime.date object to string """
    return '%04d-%02d-%02d' % (d.year, d.month, d.day)

def root_url_prefix(app, prefix_key):
    """ return the url prefix """
    return app.config["ROOT_URL_PREFIX"] + app.config[prefix_key]

def send_reset_token(user, token):
    send_mail(
        subject="Reset password ",
        recipient=user.email,
        body=flask_render_template(
            "user/reset_password.txt",
            user=user,
            token=token
        )
    )

def send_mail(subject, recipient, body, as_attachment=False):
    """ send mail """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender = current_app.config["MAIL_SENDER"]
    smtpserver = current_app.config["MAIL_SERVER"]
    username = current_app.config["MAIL_USERNAME"]
    password = current_app.config["MAIL_PASSWORD"]

    # attachment
    if as_attachment:
        msgroot = MIMEMultipart('related')
        msgroot['Subject'] = subject
        att = MIMEText(body, 'base64', 'utf-8')
        att["Content-Type"] = 'text/plain'
        att["Content-Disposition"] = \
            'attachment; filename="%s.txt"' % (time.strftime("%Y%m%d"))
        msgroot.attach(att)
    else:
        msgroot = MIMEText(body, 'base64', 'utf-8')
        msgroot['Subject'] = subject

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, recipient, msgroot.as_string())
    smtp.quit()
