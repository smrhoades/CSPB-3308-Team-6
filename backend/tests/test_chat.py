import pytest
from flask import g, session
from message_app.chat import handle_message


def test_chat_page(client):
    response = client.get('/chat')
    assert response.status_code == 200
    