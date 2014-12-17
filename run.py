"""
    productporter
    ~~~~~~~~~~~~~~~~~~~~

    helper for uwsgi

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
from productporter.app import create_app
from productporter.configs.production import ProductionConfig

app = create_app(config=ProductionConfig())
