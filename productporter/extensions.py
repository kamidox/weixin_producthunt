# -*- coding: utf-8 -*-
"""
    productporter.extensions
    ~~~~~~~~~~~~~~~~~~~~

    The extensions that are used by ProductPorter.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.themes2 import Themes
from flask.ext.cache import Cache

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# Themes
themes = Themes()

# Caching
cache = Cache()
