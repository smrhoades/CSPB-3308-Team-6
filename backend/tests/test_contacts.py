import pytest
from datetime import datetime
from http import HTTPStatus
from message_app.db import get_db, has_contact, get_user_by_name

# parse date string
def pds(date_str):
    return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')

def test_contacts(client, auth):
    auth.login()
    response = client.get('/contacts')
    contacts = response.json['contacts_data']
    contact1 = contacts[0]
    contact2 = contacts[1]
    
    # Check that data has correct fields
    assert 'contact_id' in contact1
    assert 'contact_name' in contact1
    assert 'contact_uuid' in contact1
    
    # Check that the correct contacts have been retrieved
    assert 'test2' in contact1['contact_name']
    assert 'test3' in contact2['contact_name']
    
    # Check messages 
    messages = response.json['message_data']
    assert len(messages) == 3
    assert pds(messages[0]['created_at']) > pds(messages[1]['created_at']) > pds(messages[2]['created_at'])
    # Check only messages to/from 'other' and 'test2'
    for i in range(len(messages)):
        assert messages[i]['user_from_name'] in [contact1['contact_name'], contact2['contact_name']] or messages[i]['user_to_name'] in [contact1['contact_name'], contact2['contact_name']]

def test_contacts_no_login(client):
    response = client.get('/contacts')
    
    # Check for a redirect response (302)
    assert response.status_code == HTTPStatus.FOUND
    
    # Check that client is redirected to login page
    assert 'auth/login' in response.location

@pytest.mark.parametrize(
        ('username', 'message'), (
            ('test', 'cannot add self as a contact'),
            ('xx', 'user xx not found'),
            ('test2', 'test2 already in contacts'),
            ('island', 'success')
            ))
def test_add_contact_validation(client, auth, username, message):
    auth.login()
    response = client.post('/contacts', json={'username': username})
    assert message in response.json['message']

def test_add_contact_db_write(app, client, auth):
    auth.login()
    client.post('/contacts', json={'username': 'island'})
    with app.app_context():
        db = get_db()
        user = get_user_by_name(db, 'test')
        contact = get_user_by_name(db, 'island')
        assert has_contact(db, user, contact)