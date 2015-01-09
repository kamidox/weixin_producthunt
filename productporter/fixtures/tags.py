# -*- coding: utf-8 -*-
"""
    productporter.fixtures.tags
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The fixtures module for our tags.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""


from collections import OrderedDict


fixture = OrderedDict((
    ('iOS', {
        'description': 'iOS application'
    }),
    ('Android', {
        'description': 'Android application'
    }),
    ('Web', {
        'description': 'Web application'
    }),
    ('Development', {
        'description': 'Development tools'
    }),
    ('Design', {
        'description': 'Design patterns and tools'
    }),
))
