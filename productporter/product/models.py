# -*- coding: utf-8 -*-
"""
    productporter.user.models
    ~~~~~~~~~~~~~~~~~~~~

    This module provides the models for the user.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import re
import datetime
from productporter.extensions import db

# markdown template
_MD_TEMPLATE = """## [%s](%s)
> %s

![screenshot](%s)
"""

class Product(db.Model):
    __tablename__ = "products"


    # field map between Product and ProductHuntAPI JSON data
    FIELD_MAP = {
        "postid": "id",
        "name": "name",
        "tagline": "tagline",
        "date": "day",
        "redirect_url": "redirect_url",
        "discussion_url": "discussion_url",
        "screenshot_url": "screenshot_url[850px]",
        "votes_count": "votes_count",
        "comments_count": "comments_count",
    }

    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    tagline = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)

    redirect_url = db.Column(db.String(256), nullable=False)
    discussion_url = db.Column(db.String(256), nullable=False)
    screenshot_url = db.Column(db.String(256), nullable=False)

    votes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)

    # translate infomation 
    # ctagline is a one line translate information
    ctagline = db.Column(db.Text)
    # cintro is a detail introduct of the product
    cintro = db.Column(db.Text)

    # user who translate this product
    translating_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    translating_user = db.relationship('User', 
                                    lazy="joined",
                                    backref="product_translating", uselist=False,
                                    foreign_keys=[translating_user_id])

    # user who review this product
    reviewing_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewing_user = db.relationship('User', 
                                    lazy="joined",
                                    backref="product_reviewing", uselist=False,
                                    foreign_keys=[reviewing_user_id])

    # user who write introduce article to this product
    introducing_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    introducing_user = db.relationship('User', 
                                    lazy="joined",
                                    backref="product_introducing", uselist=False,
                                    foreign_keys=[introducing_user_id])

    # user id who translate this product
    translate_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    review_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    introduce_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """Saves a product"""
        if not self.cintro:
            self.cintro = _MD_TEMPLATE % (self.name, self.redirect_url, \
                self.tagline, self.screenshot_url)
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def from_json(cls, json):
        """
        Create from json data or update the exist one
        """
        p = cls.query.filter(cls.postid==json['id']).first()
        if not p:
            p = cls()
        for k, v in cls.FIELD_MAP.items():
            if '[' in v:
                m = re.search(r"^(.+)\[(.+)\]$", v)
                setattr(p, k, json[m.group(1)][m.group(2)])
            elif k == 'date':
                ymd = json[v].split('-')
                p.date = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
            else:
                setattr(p, k, json[v])
        return p
