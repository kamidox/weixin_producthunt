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

    ## Instance path is used to store database and config file
    INSTANCE_PATH = '/tmp'

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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_PATH + '/' + \
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
    LOGIN_VIEW = "user.login"
    REAUTH_VIEW = "user.reauth"
    LOGIN_MESSAGE_CATEGORY = "error"

    # URL Prefixes. If you deply application on example.com/app1/app2
    # then, the value here should be app1/app2
    ROOT_URL_PREFIX = ""
    # Blueprints URL Prefixs.
    PRODUCT_URL_PREFIX = ""
    WEIXIN_URL_PREFIX = "/weixin"
    USER_URL_PREFIX = "/user"

    ## Mail
    MAIL_SERVER = "localhost"
    MAIL_USERNAME = "noreply@example.org"
    MAIL_PASSWORD = ""
    MAIL_SENDER = "noreply@example.org"
    # The user who should recieve the error logs
    ADMINS = ["your_admin_user@gmail.com"]

    ## ProductHuntAPI key and secret
    PH_API_KEY = "your_producthunt_api_key"
    PH_API_SECRET = "your_producthunt_api_secret"
    ## if you do not have ProductHuntAPI key and secret plesae use local data
    ## to run unit test
    PH_API_USE_SAMPLE_DATA = False

    ## weixin token
    WEIXIN_UNITTEST = False
    WEIXIN_TOKEN = "your_weixin_token"

    # Caching
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 60

    ## theme
    DEFAULT_THEME = ""

    WEIBO_APP_KEY = '' # your weibo app key
    WEIBO_APP_SECRET = '' # your weibo app secret

    # qiniu key
    # if you change bucket ,you should also change js qiniu config
    QINIU_ACCESS_KEY = ""
    QINIU_SECRET_KEY = ""
    QINIU_BUCKET = ""
## application common setting

porter_config = {
    'PRODUCT_PER_PAGE': 10,         # 10 products per page
    'ONLINE_LAST_MINUTES': 10       # 10 minutes online
}
