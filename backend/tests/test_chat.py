import pytest
from flask import g, session

def test_chat_page(client):
    response = client.get('/chat')
    assert response.status_code == 200
    