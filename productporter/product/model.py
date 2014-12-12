# -*- coding: utf-8 -*-
"""
    productporter.user.models
    ~~~~~~~~~~~~~~~~~~~~

    This module provides the models for the user.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime
from productporter.extensions import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    tagline = db.Column(db.Text, nullable=False)
    date = db.Column(db.Datetime, default=datetime.utcnow())

    redirect_url = db.Column(db.String(256), nullable=False)
    discussion_url = db.Column(db.String(256), nullable=False)
    screenshot_url = db.Column(db.String(256), nullable=False)

    votes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)

    # translate infomation
    cname = db.Column(db.String(128))
    ctagline = db.Column(db.Text)

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """Saves a product"""
        db.session.add(self)
        db.session.commit()
        return self

