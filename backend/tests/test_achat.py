from sqlalchemy import select
from message_app.db import get_db
from message_app.data_classes import User, Message
from datetime import datetime, timezone
from conftest import AuthActions

def create_room_name(user_uuid, contact_uuid):
    """ helper for creating room names """
    return min(user_uuid+contact_uuid, contact_uuid+user_uuid)

def create_test_datetime(year=2024, month=1, day=1, hour=1, minute=1, second=0):
    """ helper function for creating timestamps """
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)

def test_socketio_handlers(app, client, auth):
    """
        This is a very long test because I can't get multiple tests to work. 
        So all testing of handlers is done within this function. 
        
        Tests:
            test_websocket_socket_nologin
                - an anonymous user cannot open a connection
            test_websocket_connect
                - a logged-in user can open a real-time connection
            test_join_room
                - user 'test' can join a room
                - user 'test2' can join the same room
            test_send_message
                - 'test' sends message to 'test2'
                - message is stored in db
            test_message_db_failure_response
                - an error message is received when message fails to commit to db
    """
    #--------------------------------------------------------------------------
    # begin test_websocket_socket_nologin
    #    an anonymous user cannot open a connection
    #--------------------------------------------------------------------------
    app_socketio = app.extensions['socketio']

    # User must be logged in to connect
    socketio_client = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)
    try:
        assert not socketio_client.is_connected()
    finally:
        # Ensure cleanup happens even if test fails
        if socketio_client.is_connected(namespace='/chat'):
            socketio_client.disconnect(namespace='/chat')
    
    #--------------------------------------------------------------------------
    # end test_websocket_socket_nologin
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # begin test_websocket_connect
    #    a logged-in user can open a real-time connection
    #--------------------------------------------------------------------------
    # Initialize testing clients
    auth.login()
    socketio_client = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)
    assert socketio_client.is_connected(namespace='/chat')
            
    # Create second client for 'test2' and login
    client2 = app.test_client()
    AuthActions(client2).login(username='test2', password='test2')
    socketio_client2 = app_socketio.test_client(app, namespace='/chat', flask_test_client=client2)
    assert socketio_client2.is_connected(namespace='/chat')
    #--------------------------------------------------------------------------
    # end test_websocket_connect
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # begin test_join_room
    #    user 'test' can join a room
    #    user 'test2' can join the same room
    #--------------------------------------------------------------------------
    with app.app_context():
        db = get_db()
        test_user = db.scalar(select(User).where(User.user_name=='test'))
        test2 = db.scalar(select(User).where(User.user_name=='test2'))
    
    room_name = create_room_name(test_user.uuid, test2.uuid)

    # Emit join room event
    socketio_client.emit('join', {'room': room_name}, namespace='/chat')

    # Check for confirmation response
    received = socketio_client.get_received(namespace='/chat')
    assert len(received) == 1
    assert received[0]['name'] == 'room_joined'
    assert received[0]['args'][0]['room'] == room_name
    
    # test2 joins same room
    room_name = create_room_name(test2.uuid, test_user.uuid)
    socketio_client2.emit('join', {'room': room_name}, namespace='/chat')
    received = socketio_client2.get_received(namespace='/chat')
    assert len(received) == 1
    assert received[0]['name'] == 'room_joined'
    assert received[0]['args'][0]['room'] == room_name
    
    #--------------------------------------------------------------------------
    # end test_join_room
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # begin test_send_message
    #    users in same room can send/receive a message
    #    message is stored in db
    #--------------------------------------------------------------------------

    # test1 sends message to test2
    socketio_client.send({'recipient_user_name': 'test2',
                        'message': 'Did you get my long message?'}, 
                        json=True, namespace='/chat')
    received = socketio_client.get_received(namespace='/chat')
    received2 = socketio_client2.get_received(namespace='/chat')
    assert received == received2 # message should be broadcast
    assert len(received) == 1
    assert received[0]['name'] == 'message'
    assert received[0]['args']['message'] == 'Did you get my long message?'
    assert received[0]['args']['sender'] == 'test'
    assert received[0]['args']['recipient_user_name'] == 'test2'
    assert len(received[0]['args']['created_at']) > 0
    assert received[0]['namespace'] == '/chat'
    
    # message should be stored in db
    with app.app_context():
        db = get_db()
        msg = db.scalar(select(Message).where(Message.user_from==1)
                .where(Message.user_to==2)
                .where(Message.text.startswith("Did you get")))
        
        assert msg != None
        assert msg.created_at < datetime.now()
    #--------------------------------------------------------------------------
    # end test_send_message
    #--------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------
    # begin test_message_db_failure_response
    #    an error message is received when message fails to commit to db
    #--------------------------------------------------------------------------
    import unittest.mock
    
    with app.app_context():
        db = get_db()
        room_name = min(test_user.uuid+test2.uuid, test2.uuid+test_user.uuid)
        
        # Mock db.commit to raise an exception
        with unittest.mock.patch.object(db, 'commit', side_effect=Exception('Database connection lost')):
            # Attempt to send message
            socketio_client.send({'recipient_user_name': 'test2',
                                'message': 'This should fail'}, 
                                json=True, namespace='/chat')
            
            # Check for error response
            received = socketio_client.get_received(namespace='/chat')
            assert len(received) == 1
            assert received[0]['name'] == 'error'
            assert 'Failed to send message' in received[0]['args'][0]['message']
    #--------------------------------------------------------------------------
    # end test_message_db_failure_response
    #--------------------------------------------------------------------------
    
    socketio_client.disconnect(namespace='/chat')
    socketio_client2.disconnect(namespace='/chat')
#------------------------------------------------------------------------------
# end test_socketio_handlers
#------------------------------------------------------------------------------

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

        contact_uuid = db.scalar(select(User.uuid).filter(User.user_name=='test2'))
        
        response = client.get(f'/chat/{contact_uuid}')
        
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

#------------------------------------------------------------------------------
# Commented-out code in this section are the handler tests broken up into
# different test functions. They will pass when run individually but not when
# run in a series. 
#------------------------------------------------------------------------------

# def test_websocket_connect(app, client, auth):
#     app_socketio = app.extensions['socketio']

#     # # User must be logged in to connect
#     socketio_client = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)
#     try:
#         assert not socketio_client.is_connected()

#         auth.login()

#         # After login - should be accepted
#         socketio_client_auth = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)
#         assert socketio_client_auth.is_connected(namespace='/chat')
#         socketio_client_auth.disconnect(namespace='/chat')
#     finally:
#         # Ensure cleanup happens even if test fails
#         if socketio_client.is_connected(namespace='/chat'):
#             socketio_client.disconnect(namespace='/chat')
    
# def test_join_room(app, client, auth):
#     with app.app_context():
#         db = get_db()
#         test_user = db.scalar(select(User).where(User.user_name=='test'))
#         test2 = db.scalar(select(User).where(User.user_name=='test2'))

#     auth.login()
#     app_socketio = app.extensions['socketio']
#     socketio_client = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)

#     assert socketio_client.is_connected(namespace='/chat')

#     def create_room_name(user_uuid, contact_uuid):
#         return min(user_uuid+contact_uuid, contact_uuid+user_uuid)
    
#     room_name = create_room_name(test_user.uuid, test2.uuid)

#     # Emit join room event
#     socketio_client.emit('join', {'room': room_name}, namespace='/chat')

#     # Check for confirmation response
#     received = socketio_client.get_received(namespace='/chat')
#     assert len(received) == 1
#     assert received[0]['name'] == 'room_joined'
#     assert received[0]['args'][0]['room'] == room_name
    
#     # Create second client and login test2
#     client2 = app.test_client()
#     AuthActions(client2).login(username='test2', password='test2')
    
#     socketio_client2 = app_socketio.test_client(app, namespace='/chat', flask_test_client=client2)
    
#     assert socketio_client2.is_connected(namespace='/chat')
    
#     # test2 joins same room
#     room_name = create_room_name(test2.uuid, test_user.uuid)
#     socketio_client2.emit('join', {'room': room_name}, namespace='/chat')
#     received = socketio_client2.get_received(namespace='/chat')
#     assert len(received) == 1
#     assert received[0]['name'] == 'room_joined'
#     assert received[0]['args'][0]['room'] == room_name
    
#     # test1 sends message to test2
#     socketio_client.send({'recipient_user_name': 'test2',
#                           'message': 'Did you get my long message?'}, 
#                           json=True, namespace='/chat')
#     received = socketio_client.get_received(namespace='/chat')
#     received2 = socketio_client2.get_received(namespace='/chat')
#     assert received == received2 # message should be broadcast
#     assert len(received) == 1
#     assert received[0]['name'] == 'message'
#     assert received[0]['args']['message'] == 'Did you get my long message?'
#     assert received[0]['args']['sender'] == 'test'
#     assert received[0]['args']['recipient_user_name'] == 'test2'
#     assert len(received[0]['args']['created_at']) > 0
#     assert received[0]['namespace'] == '/chat'
    
#     # message should be stored in db
#     with app.app_context():
#         db = get_db()
#         msg = db.scalar(select(Message).where(Message.user_from==1)
#                 .where(Message.user_to==2)
#                 .where(Message.text.startswith("Did you get")))
        
#         assert msg != None
#         assert msg.created_at < datetime.now()
        
#     socketio_client.disconnect(namespace='/chat')
#     socketio_client2.disconnect(namespace='/chat')

# def test_message_db_failure_response(app, client, auth):
#     """Test that database failures during message sending result in error responses"""
#     import unittest.mock
    
#     auth.login()
#     app_socketio = app.extensions['socketio']
#     socketio_client = app_socketio.test_client(app, namespace='/chat', flask_test_client=client)
    
#     assert socketio_client.is_connected(namespace='/chat')
    
#     with app.app_context():
#         db = get_db()
#         test_user = db.scalar(select(User).where(User.user_name=='test'))
#         test2 = db.scalar(select(User).where(User.user_name=='test2'))
#         room_name = min(test_user.uuid+test2.uuid, test2.uuid+test_user.uuid)
        
#         # Join room first
#         socketio_client.emit('join', {'room': room_name}, namespace='/chat')
#         received = socketio_client.get_received(namespace='/chat')
#         assert len(received) == 1
        
#         # Mock db.commit to raise an exception
#         with unittest.mock.patch.object(db, 'commit', side_effect=Exception('Database connection lost')):
#             # Attempt to send message
#             socketio_client.send({'recipient_user_name': 'test2',
#                                   'message': 'This should fail'}, 
#                                   json=True, namespace='/chat')
            
#             # Check for error response
#             received = socketio_client.get_received(namespace='/chat')
#             assert len(received) == 1
#             assert received[0]['name'] == 'error'
#             assert 'Failed to send message' in received[0]['args'][0]['message']
    
#     socketio_client.disconnect(namespace='/chat')
