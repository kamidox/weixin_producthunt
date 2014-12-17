# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import json
from productporter.product.models import Product

def test_view_empty_posts(app, database, test_client, server_url):
    """Test to show empty product posts page"""
    r = test_client.get(server_url + '/product/posts')
    assert r.status_code == 200

def test_view_sample_posts(app, test_client, db_posts, some_day, server_url):
    """Test to show product posts page"""
    r = test_client.get(server_url + '/product/posts?day=' + str(some_day))
    assert r.status_code == 200

def test_translate(app, test_client, db_posts, server_url):
    """Test to aquire translation request and commmit translation"""
    p = Product.query.filter().first();
    assert p is not None

    url = server_url + '/product/translate'
    param = {'postid': p.postid}
    invalid_param = {'postid': 'non-exist-postid'}

    # test to aquire translation
    r = test_client.get(url, query_string=param)
    assert r.status_code == 200
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'success'

    # test to aquire translation on a non-exist post
    r = test_client.get(url, query_string=invalid_param)
    assert r.status_code == 404

def test_translate_commit(app, test_client, db_posts, server_url):
    """Test to aquire translation request and commmit translation"""
    p = Product.query.filter().first();
    assert p is not None

    url = server_url + '/product/translate'
    param = {'postid': p.postid}

    # test to commit translation
    jsondata = {
        'postid': p.postid,
        'ctagline': 'my awesome translation'
    }
    r = test_client.post(url, data=json.dumps(jsondata), \
        query_string=param, content_type='application/json')
    assert r.status_code == 200
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'success'
    assert jsondata['ctagline'].find('my awesome translation') >= 0

    # test to post invalid json data
    r = test_client.post(url, data='not a json data', \
        content_type='application/json')
    assert r.status_code == 405
    jsondata = json.loads(r.data)
    assert jsondata['status'] == 'error'







