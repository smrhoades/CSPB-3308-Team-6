import pytest
from flask import g, session

def test_chat_page(client):
    # Page renders and contains static details about chat page
    response = client.get('/chat')
    assert response.status_code == 200
    assert b"Chat" in response.data
    return
    
def test_chat_page_send_button(client):
    # There is a text box and button for sending new messages
    response = client.get('/chat')
    assert b"input type='text' id='messageInput'" in response.data
    assert b"button onclick='sendMessage()'" in response.data
    return

def test_chat_page_profile_link(client):
    # There is a link to the profile page
    response = client.get('/chat')
    assert b"a href='/profile'" in response.data
    return

def test_chat_page_logout_link(client):
    # There is a link to the logout page
    response = client.get('/chat')
    assert b"a href='/logout'" in response.data
    return
    
def test_empty_chat_page(client):
    # Page renders even if there is no chat history
    response = client.get('/chat')
    assert response.status_code == 200
    assert b"p id='received_messages'" in response.data
    
def test_self_message(client):
    # Can see message sent by self in chat log
    response = client.get('/chat')
    assert b"my message" in response.data
    return

def test_contact_message(client):
    # Can see message sent by contact in chat log
    response = client.get('/chat')
    assert b"your message" in response.data
    return

def test_full_chat_page(client):
    # Page renders and can see chat history including from self and from contact
    response = client.get('/chat')
    assert response.status_code == 200
    assert b"p id='received_messages'" in response.data
    assert b"my historical message" in response.data
    assert b"your historical message" in response.data

def test_saveMessageToDb():
    # Messages are sent to the DB
    return

def test_chatGetHistoryFromDb():
    # History is get from the DB
    return
    
