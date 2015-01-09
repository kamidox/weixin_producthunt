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
from productporter.extensions import db, cache
from productporter._compat import max_integer

# markdown template
_MD_TEMPLATE = """## [%s](%s)
> %s

![screenshot](%s)
"""

products_tags = db.Table(
    'products_tags',
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id')),
    db.Column('product_postid', db.Integer(), db.ForeignKey('products.postid')))

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text)

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """Saves a tag"""
        db.session.add(self)
        db.session.commit()
        Tag.invalidate_cache()
        return self

    def delete(self):
        """Deletes a tag"""
        db.session.delete(self)
        db.session.commit()
        Tag.invalidate_cache()
        return self

    @classmethod
    @cache.memoize(timeout=max_integer)
    def tag_names(cls, limit):
        """return the all tags name array"""

        tags = Tag.query.order_by(Tag.id.asc()).limit(limit).offset(0).all()
        tagnames = []
        for tag in tags:
            tagnames.append(tag.name)
        return tagnames

    @classmethod
    def names(cls, limit=20):
        """return tag name array"""

        return cls.tag_names(limit)

    @classmethod
    def invalidate_cache(cls):
        """Invalidates this objects cached metadata."""

        cache.delete_memoized(cls.tag_names)

    @classmethod
    def from_name(cls, name):
        """
        Create from tag from name or return the tag with the specific name
        """
        tag = cls.query.filter(cls.name==name).first()
        if not tag:
            tag = cls(name=name)
            tag.save()
        return tag

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
    ctagline_locked = db.Column(db.Boolean, default=False)
    ctagline_locked_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ctagline_locked_user = db.relationship('User',
                                    lazy="joined", uselist=False,
                                    foreign_keys=[ctagline_locked_user_id])
    # cintro is a detail introduct of the product
    cintro = db.Column(db.Text)
    cintro_locked = db.Column(db.Boolean, default=False)
    cintro_locked_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cintro_locked_user = db.relationship('User',
                                    lazy="joined", uselist=False,
                                    foreign_keys=[cintro_locked_user_id])
    # user who translate this product
    editing_ctagline_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    editing_ctagline_user = db.relationship('User',
                                    lazy="joined",
                                    backref="product_translating", uselist=False,
                                    foreign_keys=[editing_ctagline_user_id])

    # user who write introduce article to this product
    editing_cintro_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    editing_cintro_user = db.relationship('User',
                                    lazy="joined",
                                    backref="product_introducing", uselist=False,
                                    foreign_keys=[editing_cintro_user_id])

    tags = db.relationship('Tag',
                    secondary=products_tags,
                    primaryjoin=(products_tags.c.product_postid == postid),
                    backref=db.backref('products', lazy='dynamic'),
                    lazy='dynamic')

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

    def add_tag(self, tag):
        """Adds the product to the `tag` if he isn't in it.

        :param tag: The tag which should be added to the product.
        """

        if not self.has_tag(tag):
            self.tags.append(tag)
            return self

    def remove_tag(self, tag):
        """Removes the product from the `tag` if it is in it.

        :param tag: The tag which should be removed from the product.
        """

        if self.has_tag(tag):
            self.tags.remove(tag)
            return self

    def has_tag(self, tag):
        """Returns True if the product has the specified tag

        :param tag: The tag which should be checked.
        """

        return self.tags.filter(products_tags.c.tag_id == tag.id).count() > 0

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
