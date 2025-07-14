def test_contacts(client, auth):
    auth.login()
    response = client.get('/contacts')
    contacts = response.json.contacts_data
    contact1 = contacts[0]
    contact2 = contacts[1]
    assert 'other' in contact1.contact_name
    assert 'test2' in contact2.contact_name
    
    assert "test message 1" in contact1.recent_message.text
    assert contact2.recent_message.text is None
    
