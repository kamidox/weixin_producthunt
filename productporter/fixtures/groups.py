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
        'member': False,
        'guest': False,
        'perm_translate': True,
        'perm_comment': True,
        'perm_review': True,
        'perm_report': True,
        'perm_topic': True,
        'perm_setgroup': True,
    }),
    ('Moderator', {
        'description': 'The Moderator Group',
        'admin': False,
        'mod': True,
        'member': False,
        'guest': False,
        'perm_translate': True,
        'perm_comment': True,
        'perm_review': True,
        'perm_report': True,
        'perm_topic': True,
        'perm_setgroup': False,
    }),
    ('Member', {
        'description': 'The Member Group',
        'admin': False,
        'mod': False,
        'member': True,
        'guest': False,
        'perm_translate': True,
        'perm_comment': True,
        'perm_review': True,
        'perm_report': False,
        'perm_topic': False,
        'perm_setgroup': False,
    }),
    ('Guest', {
        'description': 'The Guest Group',
        'admin': False,
        'mod': False,
        'member': False,
        'guest': False,
        'perm_translate': False,
        'perm_comment': False,
        'perm_review': False,
        'perm_report': False,
        'perm_topic': False,
        'perm_setgroup': False,
    })
))
