import pytest
from http import HTTPStatus
from flask import g, session
from message_app.db import get_db

from message_app.data_classes import User

def test_register(client, app):
    response = client.post(
        '/auth/register', json={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:5173"
    assert 'success' in response.json['status']

    with app.app_context():
        user = get_db().query(User).filter_by(user_name='a').first()
        assert user is not None

@pytest.mark.parametrize(('username', 'password', 'status_code', 'message'), (
    ('', '', HTTPStatus.OK, 'Username is required.'),
    ('a', '', HTTPStatus.OK, 'Password is required.'),
    ('test', 'test', HTTPStatus.CONFLICT, 'already registered')
))
def test_register_validate_input(client, username, password, status_code, message):
    response = client.post(
        '/auth/register',
        json={'username': username, 'password': password}
    )
    assert response.status_code == status_code
    assert message in response.json['error']

def test_login(client, auth):
    auth.login()
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


