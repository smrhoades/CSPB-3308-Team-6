import pytest
from flask import g, session

def test_chat_page(client):
    response = client.get('/chat')
    assert response.status_code == 200
    
def test_saveMessageToDb():
    #TODO
    return
    
def test_history_page(client):
    data = {'sender': 1,'receiver': 4}
    response = client.post('/history', json=data)
    assert response.status_code == 200