from datetime import datetime

# parse date string
def pds(date_str):
    return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')

def test_contacts(client, auth):
    auth.login()
    response = client.get('/contacts')
    contacts = response.json['contacts_data']

    contact1 = contacts[0]
    contact2 = contacts[1]
    
    # Check that the correct contacts have been retrieved
    assert 'other' in contact1['contact_name']
    assert 'test2' in contact2['contact_name']
    
    # Check messages 
    messages = response.json['message_data']
    assert len(messages) == 3
    assert pds(messages[0]['created_at']) > pds(messages[1]['created_at']) > pds(messages[2]['created_at'])
    for i in range(len(messages)):
        assert messages[i]['user_from_name'] in [contact1['contact_name'], contact2['contact_name']] or messages[i]['user_to_name'] in [contact1['contact_name'], contact2['contact_name']]
    
