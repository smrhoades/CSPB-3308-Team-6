import pytest
from flask import g, session
from message_app.db import get_db

def test_home_noauth(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/auth/login'

def test_home_auth(client, auth):
    auth.login()
    response = client.get('/')
    assert response.status_code == 200
    assert b'test\'s home page' in response.data