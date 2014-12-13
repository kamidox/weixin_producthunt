# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""

from productporter.product.models import Product

def test_product_view_empty_posts(app, database, test_client):
    """Test to show empty product posts page"""
    server = 'http://' + app.config['SERVER_NAME']
    r = test_client.get(server + '/product/posts')
    assert r.status_code == 200

def test_product_view_old_posts(app, database, test_client, old_posts, old_day):
    """Test to show product posts page"""
    for jsondata in old_posts:
        pi = Product.query.filter(Product.postid==jsondata['id']).first()
        assert pi is None
        pi = Product.from_json(jsondata)
        pi.save()

    server = 'http://' + app.config['SERVER_NAME']
    r = test_client.get(server + '/product/posts?day=' + str(old_day))
    assert r.status_code == 200
