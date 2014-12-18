"""
    productporter.configs.testing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This is the ProductPorter's testing config.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
try:
    from productporter.configs.development import DevelopmentConfig as Config
except ImportError:
    from productporter.configs.default import DefaultConfig as Config

class TestingConfig(Config):

    # Indicates that it is a testing environment
    DEBUG = False
    TESTING = True

    SERVER_NAME = "localhost:5000"

    # This will print all SQL statements
    SQLALCHEMY_ECHO = False

    # Security
    SECRET_KEY = "SecretKeyForSessionSigning"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

