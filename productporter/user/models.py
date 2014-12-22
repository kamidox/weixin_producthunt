# -*- coding: utf-8 -*-
"""
    productporter.user.models
    ~~~~~~~~~~~~~~~~~~~~

    This module provides the models for the user.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from productporter._compat import max_integer
from productporter.extensions import db, cache


groups_users = db.Table(
    'groups_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')))


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)

    # Group types
    admin = db.Column(db.Boolean, default=False, nullable=False)
    mod = db.Column(db.Boolean, default=False, nullable=False)
    member = db.Column(db.Boolean, default=False, nullable=False)
    guest = db.Column(db.Boolean, default=False, nullable=False)

    # User permissions
    perm_translate = db.Column(db.Boolean, default=False, nullable=False)
    perm_comment = db.Column(db.Boolean, default=False, nullable=False)
    perm_review = db.Column(db.Boolean, default=False, nullable=False)
    perm_topic = db.Column(db.Boolean, default=False, nullable=False)
    perm_report = db.Column(db.Boolean, default=False, nullable=False)
    perm_setgroup = db.Column(db.Boolean, default=False, nullable=False)


    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self):
        """Saves a group"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Deletes a group"""
        db.session.delete(self)
        db.session.commit()
        return self


class User(db.Model, UserMixin):
    __tablename__ = "users"
    __searchable__ = ['username', 'email']

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    lastseen = db.Column(db.DateTime, default=datetime.utcnow())
    birthday = db.Column(db.DateTime)
    gender = db.Column(db.String(10))
    website = db.Column(db.String(200))
    location = db.Column(db.String(100))
    signature = db.Column(db.Text)
    avatar = db.Column(db.String(200))
    notes = db.Column(db.Text)

    theme = db.Column(db.String(15))

    primary_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'),
                                 nullable=False)

    primary_group = db.relationship('Group', lazy="joined",
                                    backref="user_group", uselist=False,
                                    foreign_keys=[primary_group_id])

    secondary_groups = \
        db.relationship('Group',
                        secondary=groups_users,
                        primaryjoin=(groups_users.c.user_id == id),
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')

    @property
    def url(self):
        """Returns the url for the user"""
        return url_for("user.profile", username=self.username)

    @property
    def permissions(self):
        """Returns the permissions for the user"""
        return self.get_permissions()

    @property
    def days_registered(self):
        """Returns the amount of days the user is registered."""
        days_registered = (datetime.utcnow() - self.date_joined).days
        if not days_registered:
            return 1
        return days_registered

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.username)

    def _get_password(self):
        """Returns the hashed password"""
        return self._password

    def _set_password(self, password):
        """Generates a password hash for the provided password"""
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false"""

        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, login, password):
        """A classmethod for authenticating users
        It returns true if the user exists and has entered a correct password

        :param login: This can be either a username or a email address.
        :param password: The password that is connected to username and email.
        """

        user = cls.query.filter(db.or_(User.username == login,
                                       User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def _make_token(self, data, timeout):
        s = Serializer(current_app.config['SECRET_KEY'], timeout)
        return s.dumps(data)

    def _verify_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        data = None
        expired, invalid = False, False
        try:
            data = s.loads(token)
        except SignatureExpired:
            expired = True
        except Exception:
            invalid = True
        return expired, invalid, data

    def make_reset_token(self, expiration=3600):
        """Creates a reset token. The duration can be configured through the
        expiration parameter.

        :param expiration: The time in seconds how long the token is valid.
        """
        return self._make_token({'id': self.id, 'op': 'reset'}, expiration)

    def verify_reset_token(self, token):
        """Verifies a reset token. It returns three boolean values based on
        the state of the token (expired, invalid, data)

        :param token: The reset token that should be checked.
        """

        expired, invalid, data = self._verify_token(token)
        if data and data.get('id') == self.id and data.get('op') == 'reset':
            data = True
        else:
            data = False
        return expired, invalid, data

    def add_to_group(self, group):
        """Adds the user to the `group` if he isn't in it.

        :param group: The group which should be added to the user.
        """

        if not self.in_group(group):
            self.secondary_groups.append(group)
            db.session.commit()
            self.invalidate_cache()
            return self

    def remove_from_group(self, group):
        """Removes the user from the `group` if he is in it.

        :param group: The group which should be removed from the user.
        """

        if self.in_group(group):
            self.secondary_groups.remove(group)
            db.session.commit()
            self.invalidate_cache()
            return self

    def in_group(self, group):
        """Returns True if the user is in the specified group

        :param group: The group which should be checked.
        """

        return self.secondary_groups.filter(
            groups_users.c.group_id == group.id).count() > 0

    @cache.memoize(timeout=max_integer)
    def get_permissions(self, exclude=None):
        """Returns a dictionary with all the permissions the user has.

        :param exclude: a list with excluded permissions. default is None.
        """

        exclude = exclude or []
        exclude.extend(['id', 'name', 'description'])

        perms = {}
        groups = self.secondary_groups.all()
        groups.append(self.primary_group)
        for group in groups:
            for c in group.__table__.columns:
                # try if the permission already exists in the dictionary
                # and if the permission is true, set it to True
                try:
                    if not perms[c.name] and getattr(group, c.name):
                        perms[c.name] = True

                # if the permission doesn't exist in the dictionary
                # add it to the dictionary
                except KeyError:
                    # if the permission is in the exclude list,
                    # skip to the next permission
                    if c.name in exclude:
                        continue
                    perms[c.name] = getattr(group, c.name)
        return perms

    def invalidate_cache(self):
        """Invalidates this objects cached metadata."""

        cache.delete_memoized(self.get_permissions, self)

    def save(self):
        """Saves a user"""

        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Deletes the User."""

        db.session.delete(self)
        db.session.commit()

        return self

class Guest(AnonymousUserMixin):
    @property
    def permissions(self):
        return self.get_permissions()

    def get_permissions(self, exclude=None):
        """Returns a dictionary with all permissions the user has"""
        exclude = exclude or []
        exclude.extend(['id', 'name', 'description'])

        perms = {}
        # Get the Guest group
        group = Group.query.filter_by(guest=True).first()
        for c in group.__table__.columns:
            if c.name in exclude:
                continue
            perms[c.name] = getattr(group, c.name)
        return perms
