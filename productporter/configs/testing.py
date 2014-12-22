"""
    productporter.configs.testing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This is the ProductPorter's testing config.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import os
try:
    from productporter.configs.development import DevelopmentConfig as Config
except ImportError:
    from productporter.configs.default import DefaultConfig as Config

class TestingConfig(Config):

    # Indicates that it is a testing environment
    DEBUG = False
    TESTING = True

    SERVER_NAME = "localhost:5000"

    # Get the app root path
    #            <_basedir>
    # ../../ -->  productporter/productporter/configs/base.py
    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))

    # a database named productporter.sqlite.
    #SQLALCHEMY_DATABASE_URI = "mysql://root@localhost"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
                              'productporter.sqlite'

    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    # Security
    SECRET_KEY = "SecretKeyForSessionSigning"
    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

