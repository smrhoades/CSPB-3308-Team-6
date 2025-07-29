from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from message_app.db import get_db
from message_app.data_classes import User, Contact, Message
from werkzeug.exceptions import abort
from message_app import socketio
from sqlalchemy import insert, select, func, or_
from flask_socketio import join_room, emit, send
from .decorators import contact_required

bp = Blueprint('chat', __name__)

@bp.route('/chat/<contact_uuid>', methods=['GET'])
@login_required
@contact_required
def chat(contact_uuid, contact):
    """
        Endpoint for conversation page between the client and their contact.
        The @contact_required decorator ensures that the contact exists and has 
        been added to the client's contacts. Moreover it retrieves the contact 
        (as a Contact object) from the database, making it available to this 
        function. 
        
        Returns message history between client and contact.
    """
    return get_chat_messages(contact)

def get_chat_messages(contact):
    """
        Retrieves message history between current_user and provided contact. 
        The messages are in order of creation time (earliest first)
        
        Notes on JSON fields:
        The 'is_own_message' subfield of 'messages' indicates if the message 
        originated from the client. 
        The 'is_mutual' field is true when both the client and contact have
        the added other as a contact. 
    
    Parameters
        contact: Contact object
    Returns JSON object:
        {
         'messages':
            [
                {
                    'id': Message.id,
                    'text': Message.text,
                    'sender': {
                        'id': Message.user_from,
                        'username': User.user_name
                        },
                    'recipient': {
                        'id': Message.user_from,
                        'username': User.user_name
                    },
                    'timestamp': Message.created_at.isoformat(),
                    'is_own_message': bool
                },
                ...
            ]
         'is_mutual': bool
        }
    """
    db = get_db()

    messages = db.execute(
        select(
            Message,
            User.user_name.label('sender_name')
            )
            .join(User, Message.user_from == User.id)
            .where(
                or_(
                    (Message.user_from == current_user.id) & (Message.user_to == contact.id),
                    (Message.user_from == contact.id) & (Message.user_to == current_user.id)
                    )
                )
                .order_by(Message.created_at)
    ).all()
    
    formatted_messages = []
    for message, sender_name in messages:
        recipient_name = db.scalar(select(User.user_name).where(User.id == message.user_to))
        
        formatted_messages.append({
            "id": message.id,
            "text": message.text,
            "sender": {
                "id": message.user_from,
                "username": sender_name
            },
            "recipient": {
                "id": message.user_to,
                "username": recipient_name
            },
            "timestamp": message.created_at.isoformat()
        })

    # Check whether each has added the other
    is_mutual = db.execute(
        select(func.count())
        .select_from(Contact)
        .where(
            or_(
                (Contact.user == current_user.id) & (Contact.contact == contact.id),
                (Contact.user == contact.id) & (Contact.contact == current_user.id)
            )
        )
    ).scalar() == 2

    return jsonify({'messages': formatted_messages, 'is_mutual': is_mutual})

#------------------------------------------------------------------------------
# Socket.IO handlers are defined in this section.
# These functions handle events ('connect', 'join', 'json') received from React.
#------------------------------------------------------------------------------
@socketio.on('connect', namespace='/chat')
def handle_chat_connect():
    """
        Allow real-time connections for logged-in users only.
    """
    if not current_user.is_authenticated:
        print("Rejected unauthenticated connection")
        return False
    print(f"User {current_user.user_name} connected to chat namespace")
    return True

@socketio.on('join', namespace='/chat')
def on_join(data):
    """
        data is expected to be a JSON:
            {'room': room_name}
        where room_name is calculated in the agreed way. 
        
        Puts user into the room.
        The user is obtained from the request context. 
        A confirmation message is emitted after room is joined. 
    """
    room = data['room']
    join_room(room)
    emit('room_joined', {'room': room})

# Handler for send events
@socketio.on('json', namespace='/chat')
def on_message(json):
    """
        Handler for receiving messages in JSON form.
        The receiveced JSON is expected to have the following form: 
            {
             'recipient_user_name': ...,
             'message': ...
            }
            
        The message is stored in the database and a JSON is broadcast to all
        clients in the room:
            {
             'recipient_user_name': ...,
             'message': ...,
             'sender': ...,
             'created_at': ...
            }
            
        An error message is emitted if the db write fails. 
    """
    # TO DO: Validate message content (non-empty, length limits)
    print('received json: ' + str(json))
    sender = current_user.user_name
    msg = json['message']
    recipient_user_name = json['recipient_user_name']

    db = get_db()
    
    try:
        recipient = db.scalar(select(User).where(User.user_name==recipient_user_name))
        created_at = db.scalar(insert(Message).values(user_from=current_user.id,
                                          user_to=recipient.id,
                                          text=msg)
                                          .returning(Message.created_at)
        )
        db.commit()
        created_at = created_at.isoformat()

        json['sender'] = sender
        json['created_at'] = created_at
        print('sending json: ' + str(json))
        room = min(current_user.uuid+recipient.uuid, recipient.uuid+current_user.uuid)
        send(json, broadcast=True, to=room)
        
    except Exception as e:
        print(f'Database error when saving message: {e}')
        db.rollback()
        emit('error', {'message': 'Failed to send message. Please try again.'}, broadcast=False)
        
@socketio.on('disconnect')
def handle_disconnect():
    """
        When a user navigates away, closes the tab, or loses internet connection,
        the WebSocket connection will automatically close.
        This handler simply prints the fact that the event happened. More useful 
        logging can be added later. 
        We can log things like the reason for the disconnect, the time of the 
        disconnect ("last seen" feature), debugging info, etc. 
    """
    print(f'User {current_user.id} disconnect from chat')