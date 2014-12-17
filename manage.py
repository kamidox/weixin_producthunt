"""
    productporter.manage
    ~~~~~~~~~~~~~~~~~~~~

    This script provides some easy to use commands for
    creating the database with or without some sample content.
    You can also run the development server with it.
    Just type `python manage.py` to see the full list of commands.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import os
import json

from flask import current_app
from flask.ext.script import (Manager, Shell, Server)

from productporter.app import create_app
from productporter.product.models import Product
from productporter.extensions import db
from productporter.utils import pull_and_save_posts
from tests.fixtures.sampledata import SAMPLE_DATA

# Use the development configuration if available
try:
    from productporter.configs.development import DevelopmentConfig as Config
except ImportError:
    from productporter.configs.default import DefaultConfig as Config

app = create_app(Config)
manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("localhost", port=5000))

# Add interactive project shell
def make_shell_context():
    return dict(app=current_app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def initdb():
    """Creates the database."""
    db.create_all()

@manager.command
def dropdb():
    """Deletes the database"""
    db.drop_all()

@manager.command
def createall():
    """Creates the database."""
    db.drop_all()
    db.create_all()
    jsondata = json.loads(SAMPLE_DATA)
    some_posts = jsondata['posts']
    for p in some_posts:
        pi = Product.from_json(p)
        pi.save()
    print('pull %d posts' % (len(some_posts)))

if __name__ == "__main__":
    manager.run()

