# -*- coding: utf-8 -*-
"""
    productporter.app
    ~~~~~~~~~~~~~~~~~

    manages the app creation and configuration process

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging

from flask import Flask

from productporter.weixin.view import weixin
# extensions
from productporter.extensions import db
# default config
from productporter.configs.default import DefaultConfig

def create_app(config=None):
    """
    Creates the app.
    """
    static_url_path = ''
    if config is None:
        static_url_path = DefaultConfig.ROOT_URL_PREFIX + '/static'
    else:
        static_url_path = config.ROOT_URL_PREFIX + '/static'
    # Initialize the app
    app = Flask("ProductPorter", static_url_path=static_url_path)

    # Use the default config and override it afterwards
    app.config.from_object('productporter.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)
    # try to update the config via the environment variable
    app.config.from_envvar("PRODUCTPORTER_SETTINGS", silent=True)

    configure_blueprints(app)
    configure_extensions(app)
    configure_template_filters(app)
    configure_context_processors(app)
    configure_before_handlers(app)
    configure_errorhandlers(app)
    configure_logging(app)

    return app

def configure_blueprints(app):
    """
    Configures the blueprints
    """
    app.register_blueprint(weixin, url_prefix=app.config["WEIXIN_URL_PREFIX"])

def configure_extensions(app):
    """
    Configures the extensions
    """

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Themes
    # themes.init_themes(app, app_identifier="productporter")

    # Flask-Login
    # login_manager.login_view = app.config["LOGIN_VIEW"]
    # login_manager.refresh_view = app.config["REAUTH_VIEW"]
    # login_manager.anonymous_user = Guest

    # @login_manager.user_loader
    # def load_user(id):
    #     """
    #     Loads the user. Required by the `login` extension
    #     """
    #     user = db.session.query(User).filter(User.id == id).first()

    #     if u:
    #         return user
    #     else:
    #         return None

    # login_manager.init_app(app)


def configure_template_filters(app):
    """
    Configures the template filters
    """
    pass


def configure_context_processors(app):
    """
    Configures the context processors
    """
    pass

def configure_before_handlers(app):
    """
    Configures the before request handlers
    """
    pass


def configure_errorhandlers(app):
    """
    Configures the error handlers
    """
    # @app.errorhandler(403)
    # def forbidden_page(error):
    #     return render_template("errors/forbidden_page.html"), 403

    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template("errors/page_not_found.html"), 404

    # @app.errorhandler(500)
    # def server_error_page(error):
    #     return render_template("errors/server_error.html"), 500


def configure_logging(app):
    """
    Configures logging.
    """

    logs_folder = os.path.join(app.root_path, "logs")
    from logging.handlers import SMTPHandler
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    info_log = os.path.join(logs_folder, app.config['INFO_LOG'])

    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(logs_folder, app.config['ERROR_LOG'])

    error_file_handler = logging.handlers.RotatingFileHandler(
        error_log,
        maxBytes=100000,
        backupCount=10
    )

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    if app.config["SEND_LOGS"]:
        mail_handler = \
            SMTPHandler(app.config['MAIL_SERVER'],
                        app.config['MAIL_SENDER'],
                        app.config['ADMINS'],
                        'application error, no admins specified',
                        (
                            app.config['MAIL_USERNAME'],
                            app.config['MAIL_PASSWORD'],
                        ))

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)
