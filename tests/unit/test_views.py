# -*- coding: utf-8 -*-
"""
    productporter unit test
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
import json
from productporter.product.models import Product
from productporter.configs.testing import TestingConfig as Config
from flask import url_for

def captured_flash_message(app, recorded, **extra):
    """capture flash message for unit test"""

    def record(sender, message, category):
        recorded.append((message, category))
    from flask import message_flashed
    return message_flashed.connected_to(record, app)

def test_view_empty_posts(app, database, test_client, default_groups):
    """Test to show empty product posts page"""

    url = url_for('product.posts')
    r = test_client.get(url)
    assert r.status_code == 200

def test_view_sample_posts(app, test_client, db_posts, some_day, default_groups):
    """Test to show product posts page"""

    url = url_for('product.posts')
    param = {'day': str(some_day)}
    r = test_client.get(url, query_string=param)
    assert r.status_code == 200

def cowork_request(app, test_client, db_posts, user, moderator_user, field):
    """Test to aquire translation request and commmit translation"""

    p = Product.query.filter().first();
    assert p is not None

    url = url_for('product.translate')
    param = {'postid': p.postid, 'field': field}
    invalid_param = {'postid': 'non-exist-postid', 'field': field}

    # test to aquire translation with a guest
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 401
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'error'

    # login
    messages = []
    url = url_for('user.login')
    data = {'login': user.username, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    # aquire translate
    url = url_for('product.translate')
    param = {'postid': p.postid, 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 200
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'success'

    # login with mod user
    messages = []
    url = url_for('user.login')
    data = {'login': moderator_user.username, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    # aquire translate
    url = url_for('product.translate')
    param = {'postid': p.postid, 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 400
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'error'
    assert jsondata['error'] == '%s is editing by test_normal' % (field)

def test_translate_ctagline(app, test_client, db_posts, user, moderator_user):
    """test translate request"""
    cowork_request(app, test_client, db_posts, user, moderator_user, 'ctagline')

def test_translate_cintro(app, test_client, db_posts, user, moderator_user):
    """test introduce request"""
    cowork_request(app, test_client, db_posts, user, moderator_user, 'cintro')

def cowork_commit(app, test_client, db_posts, user, field):
    """Test to commmit cowork result"""

    p = Product.query.filter().first();
    assert p is not None

    # commit translation with guest will failed
    url = url_for('product.translate')
    jsondata = {
        'postid': p.postid,
        'field': field,
        'value': 'my awesome translation'
    }
    r = test_client.post(url, data=json.dumps(jsondata), \
        content_type='application/json', \
        follow_redirects=True)
    assert r.status_code == 401
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'error'

    # login
    messages = []
    url = url_for('user.login')
    data = {'login': user.username, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    # commit translate with login user will success
    url = url_for('product.translate')
    jsondata = {
        'postid': p.postid,
        'field': field,
        'value': 'my awesome translation'
    }
    r = test_client.post(url, data=json.dumps(jsondata), \
            content_type='application/json')
    assert r.status_code == 200
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'success'
    assert jsondata['field'] == field
    assert jsondata['value'].find('my awesome translation') >= 0
    assert jsondata['contributors'].find(user.username) >= 0

    # commit with an invalid json data will failed
    r = test_client.post(url, data='not a json data', \
        content_type='application/json')
    assert r.status_code == 405
    jsondata = json.loads(r.data)
    assert jsondata['status'] == 'error'

    # cancel commit will success
    url = url_for('product.translate')
    jsondata = {
        'postid': p.postid,
        'field': field,
        'canceled': 'true'
    }
    r = test_client.post(url, data=json.dumps(jsondata), \
            content_type='application/json')
    assert r.status_code == 200
    jsondata = json.loads(r.data)
    assert p.postid == jsondata['postid']
    assert jsondata['status'] == 'success'

def test_commit_ctagline(app, test_client, db_posts, user):
    """test to commit translate result"""

    cowork_commit(app, test_client, db_posts, user, 'ctagline')

def test_commit_cintro(app, test_client, db_posts, user):
    """test to commit translate result"""

    cowork_commit(app, test_client, db_posts, user, 'cintro')

def cowork_lock(app, test_client, db_posts, user, moderator_user, field):
    """ test lock """

    p = Product.query.filter().first();
    assert p is not None

    # login with user
    messages = []
    url = url_for('user.login')
    data = {'login': user.username, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    # lock item with user will get 403
    url = url_for('product.lock')
    param = {'postid': p.postid, 'op': 'lock', 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 403

    # login with moderator_user
    messages = []
    url = url_for('user.login')
    data = {'login': moderator_user.username, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    # lock item with non-exist item will get 404
    url = url_for('product.lock')
    param = {'postid': 'non-exist', 'op': 'lock', 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 404

    # lock item success
    url = url_for('product.lock')
    param = {'postid': p.postid, 'op': 'lock', 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 200

    # after lock item, aquire translate will failed
    url = url_for('product.translate')
    param = {'postid': p.postid, 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 403

    # unlock item success
    url = url_for('product.lock')
    param = {'postid': p.postid, 'op': 'unlock', 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 200

    # after unlock item, aquire translate will success
    url = url_for('product.translate')
    param = {'postid': p.postid, 'field': field}
    r = test_client.get(url, query_string=param, follow_redirects=True)
    assert r.status_code == 200

def test_lock_ctagline(app, test_client, db_posts, user, moderator_user):
    """ test lock ctagline """
    cowork_lock(app, test_client, db_posts, user, moderator_user, 'ctagline')

def test_lock_cintro(app, test_client, db_posts, user, moderator_user):
    """ test lock ctagline """
    cowork_lock(app, test_client, db_posts, user, moderator_user, 'cintro')

def test_user_profile(app, test_client, user):
    """test view user profile"""

    url = url_for('user.profile', username=user.username)
    r = test_client.get(url)
    assert r.status_code == 200

    url = url_for('user.profile', username='user-not-exist')
    r = test_client.get(url)
    assert r.status_code == 404

def test_login(app, test_client, user):
    """test login as user"""

    messages = []
    url = url_for('user.login')
    data = {'login': user.username, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    messages = []
    data = {'login': user.username, 'password': 'error-password'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Username or password error'

def test_register(app, test_client, default_groups):
    """test register"""

    messages = []
    url = url_for('user.register')
    data = {'username': 'test_normal',
        'email': 'test_normal@example.org',
        'password': 'test',
        'confirm_password': 'test',
        'accept_tos': 'y'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Thanks for registering'

    # register a duplicate user will failed
    messages = []
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 0

def test_forgot_and_reset_password(app, test_client, user):
    """test forget password"""

    # test for forget password
    messages = []
    url = url_for('user.forgot_password')
    data = {'email': 'test_normal@example.org'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'E-Mail sent! Please check your inbox.'

    messages = []
    data = {'email': 'not_exist@example.org'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'E-mail not exist!'

    # test for reset password
    messages = []
    token = 'invalid-token'
    url = url_for('user.reset_password', token=token)
    data = {'token': token,
        'email': user.email,
        'password': 'new_password',
        'confirm_password': 'new_password'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Your password token is invalid.'

    messages = []
    token = user.make_reset_token()
    url = url_for('user.reset_password', token=token)
    data = {'token': token,
        'email': user.email,
        'password': 'new_password',
        'confirm_password': 'new_password'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Your password has been updated.'

    # test go sign in with new password
    messages = []
    url = url_for('user.login')
    data = {'login': user.username, 'password': 'new_password'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

def test_change_email(app, test_client, user, moderator_user):
    """ test to change email and password """

    # sign in first
    messages = []
    url = url_for('user.login')
    data = {'login': user.email, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    # change email with old email not exist
    messages = []
    url = url_for('user.settings_email')
    data = {'old_email': 'not_exist@example.org',
        'new_email': 'new_email@example.org',
        'confirm_new_email': 'new_email@example.org'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 0

    # change email with new email already exist
    messages = []
    url = url_for('user.settings_email')
    data = {'old_email': user.email,
        'new_email': moderator_user.email,
        'confirm_new_email': moderator_user.email}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 0

    # change email
    messages = []
    url = url_for('user.settings_email')
    data = {'old_email': user.email,
        'new_email': 'new_email@example.org',
        'confirm_new_email': 'new_email@example.org'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Your email have been updated!'

    # test go sign in with new email
    messages = []
    url = url_for('user.login')
    data = {'login': 'new_email@example.org', 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

def test_change_password(app, test_client, user):
    """ change password """

    # sign in first
    messages = []
    url = url_for('user.login')
    data = {'login': user.email, 'password': 'test'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'

    # change password with old password not correct
    messages = []
    url = url_for('user.settings_password')
    data = {'old_password': 'invalid_old_password',
        'new_password': 'new_password',
        'confirm_new_password': 'new_password'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 0

    # change password
    messages = []
    url = url_for('user.settings_password')
    data = {'old_password': 'test',
        'new_password': 'new_password',
        'confirm_new_password': 'new_password'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Your password have been updated!'

    # sign in with new password
    messages = []
    url = url_for('user.login')
    data = {'login': user.email, 'password': 'new_password'}
    with captured_flash_message(app, messages):
        r = test_client.post(url, data=data, follow_redirects=True)
        assert r.status_code == 200
        assert len(messages) == 1
        assert messages[0][0] == 'Sign in successful'



