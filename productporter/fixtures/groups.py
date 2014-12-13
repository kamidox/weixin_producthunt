# -*- coding: utf-8 -*-
"""
    productporter.fixtures.groups
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The fixtures module for our groups.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""

from collections import OrderedDict


fixture = OrderedDict((
    ('Administrator', {
        'description': 'The Administrator Group',
        'admin': True,
        'mod': False,
        'guest': False,
        'editproduct': True,
        'deleteproduct': True,
    }),
    ('Moderator', {
        'description': 'The Moderator Group',
        'admin': False,
        'mod': True,
        'guest': False,
        'editproduct': True,
        'deleteproduct': False,
    }),
    ('Member', {
        'description': 'The Member Group',
        'admin': False,
        'mod': False,
        'guest': False,
        'editproduct': False,
        'deleteproduct': False,
    }),
    ('Guest', {
        'description': 'The Guest Group',
        'admin': False,
        'mod': False,
        'guest': False,
        'editproduct': False,
        'deleteproduct': False,
    })
))
