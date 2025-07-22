from sqlalchemy import select
from message_app.db import get_db
from message_app.data_classes import User, Message
from datetime import datetime, timezone
# from flask_socketio import SocketIO
# from message_app.__init__ import socketio

def create_test_datetime(year=2024, month=1, day=1, hour=1, minute=1, second=0):
    """ helper function for creating timestamps """
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)

def test_chat_url(app, client, auth):
    auth.login()
    with app.app_context():
        db = get_db()
    
        # Attempt to open chat with contact: 'test2'
        contact_uuid = db.scalar(select(User.uuid).filter(User.user_name=='test2'))
        response = client.get(f'/chat/{contact_uuid}')
        assert response.status_code == 200
        
        # Chat not allowed: 'test' does not have 'island' in contacts
        contact_uuid2 = db.scalar(select(User.uuid).filter(User.user_name=='island'))
        response = client.get(f'/chat/{contact_uuid2}')
        assert response.status_code == 403

def test_load_chat_history(app, client, auth):
    auth.login()
    with app.app_context():
        db = get_db()

        current_user = db.scalar(select(User).filter(User.user_name=='test'))        
        contact_uuid = db.scalar(select(User.uuid).filter(User.user_name=='test2'))
        contact_user = db.scalar(select(User).filter(User.user_name=='test2'))
        
        # Create test messages
        m1 = Message(
            user_from=current_user.id,
            user_to=contact_user.id,
            text="Hello from test user!",
            created_at = create_test_datetime(year=2024, month=1, day=1, hour=1, minute=0, second=0)
        )
        m2 = Message(
            user_from=contact_user.id,
            user_to=current_user.id,
            text="Hello back from test2!",
            created_at = create_test_datetime(year=2025, month=1, day=1, hour=1, minute=1, second=0)
        )
        m3 = Message(
            user_from=current_user.id,
            user_to=contact_user.id,
            text="long message"*20,
            created_at = create_test_datetime(year=2025, month=1, day=1, hour=1, minute=2, second=0)
        )
        
        db.add_all([m1, m2, m3])
        db.commit()

        response = client.get(f'/chat/{contact_uuid}/messages')
        
        assert response.status_code == 200
        response_data = response.get_json()
        
        assert 'messages' in response_data
        assert 'is_mutual' in response_data
        
        assert response_data['is_mutual'] == True

        messages = response_data['messages']
        assert len(messages) == 3
        
        # Check first message structure
        first_message = messages[0]
        assert 'id' in first_message
        assert 'text' in first_message
        assert 'sender' in first_message
        assert 'recipient' in first_message
        assert 'timestamp' in first_message
        
        # Check sender structure
        assert 'id' in first_message['sender']
        assert 'username' in first_message['sender']
        
        # Check recipient structure
        assert 'id' in first_message['recipient']
        assert 'username' in first_message['recipient']
        
        # Verify content of first message
        assert first_message['text'] == "Hello from test user!"
        assert first_message['sender']['username'] == 'test'
        assert first_message['recipient']['username'] == 'test2'
        
        # Verify messages are in chronological order
        assert messages[0]['text'] == "Hello from test user!"
        assert messages[1]['text'] == "Hello back from test2!"
        assert messages[2]['text'] == "long message"*20
        
        # Clean up test data
        db.delete(m1)
        db.delete(m2)
        db.delete(m3)
        db.commit()

def test_websocket_connect(app, client, auth):
    app_socketio = app.extensions['socketio']
    print(f"SocketIO access in test: {app_socketio}")
    print(f"SocketIO handlers in test: {app_socketio.handlers}")
        
    # # User must be logged in to connect
    socketio_client = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)
    assert not socketio_client.is_connected()

    auth.login()
    
    # After login - should be accepted
    socketio_client = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)
    assert socketio_client.is_connected(namespace='/chat')
    
    # auth.login()
    # socketio_client = socketio.test_client(app, namespace='/chat', flask_test_client=client)
    # print(socketio_client)

# def test_chat_page(client):
#     # Page renders and contains static details about chat page
#     response = client.get('/chat')
#     assert response.status_code == 200
#     assert b"Chat" in response.data
#     return
    
# def test_chat_page_send_button(client):
#     # There is a text box and button for sending new messages
#     response = client.get('/chat')
#     assert b"input type='text' id='messageInput'" in response.data
#     assert b"button onclick='sendMessage()'" in response.data
#     return

# def test_chat_page_profile_link(client):
#     # There is a link to the profile page
#     response = client.get('/chat')
#     assert b"a href='/profile'" in response.data
#     return

# def test_chat_page_logout_link(client):
#     # There is a link to the logout page
#     response = client.get('/chat')
#     assert b"a href='/logout'" in response.data
#     return
    
# def test_empty_chat_page(client):
#     # Page renders even if there is no chat history
#     response = client.get('/chat')
#     assert response.status_code == 200
#     assert b"p id='received_messages'" in response.data
    
# def test_self_message(client):
#     # Can see message sent by self in chat log
#     response = client.get('/chat')
#     assert b"my message" in response.data
#     return

# def test_contact_message(client):
#     # Can see message sent by contact in chat log
#     response = client.get('/chat')
#     assert b"your message" in response.data
#     return

# def test_full_chat_page(client):
#     # Page renders and can see chat history including from self and from contact
#     response = client.get('/chat')
#     assert response.status_code == 200
#     assert b"p id='received_messages'" in response.data
#     assert b"my historical message" in response.data
#     assert b"your historical message" in response.data

# def test_saveMessageToDb():
#     # Messages are sent to the DB
#     return

# def test_chatGetHistoryFromDb():
#     # History is get from the DB
#     return
    
