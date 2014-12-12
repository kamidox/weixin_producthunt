# -*- coding: utf-8 -*-
"""
    productporter.configs.default
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This is the default configuration for ProductPorter that every site should
    have. You can override these configuration variables in another class.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import os


class DefaultConfig(object):

    # Get the app root path
    #            <_basedir>
    # ../../ -->  weixin_producthunt/ProductPorter/configs/base.py
    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))

    DEBUG = False
    TESTING = False

    # Logs
    # If SEND_LOGS is set to True, the admins (see the mail configuration) will
    # recieve the error logs per email.
    SEND_LOGS = False

    # The filename for the info and error logs. The logfiles are stored at
    # weixin_producthunt/logs
    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"

    # Default Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
                              'productporter.sqlite'

    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    # Security
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # Protection against form post fraud
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    # Auth
    LOGIN_VIEW = "auth.login"
    REAUTH_VIEW = "auth.reauth"
    LOGIN_MESSAGE_CATEGORY = "error"

    # URL Prefixes.
    ROOT_URL_PREFIX = "/weixin"
    # Blueprints URL Prefixs.
    WEIXIN_URL_PREFIX = "/weixin"
    USER_URL_PREFIX = "/user"
    AUTH_URL_PREFIX = "/auth"
    ADMIN_URL_PREFIX = "/admin"

    ## Mail
    MAIL_SERVER = "localhost"
    MAIL_USERNAME = "noreply@example.org"
    MAIL_PASSWORD = ""
    MAIL_SENDER = ("Default Sender", "noreply@example.org")
    # The user who should recieve the error logs
    ADMINS = ["your_admin_user@gmail.com"]

    ## ProductHuntAPI key and secret
    PH_API_KEY = "your_producthunt_api_key"
    PH_API_SECRET = "your_producthunt_api_secret"