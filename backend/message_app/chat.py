from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from message_app.db import get_db
from message_app.data_classes import User, Contact, Message
from werkzeug.exceptions import abort
from message_app import socketio
from sqlalchemy import insert, select, exists, func, or_
from flask_socketio import join_room, emit, send
from .decorators import contact_required


bp = Blueprint('chat', __name__)

# Page load and authentication
@bp.route('/chat/<contact_uuid>', methods=['GET'])
@login_required
@contact_required
def chat(contact_uuid, contact):
    return get_chat_messages(contact)

def get_chat_messages(contact):
    """
    Structure of response:
    {'messages':
        [
            {
                'id': msg.id,
                'text': msg.text,
                'sender': {
                    'id': msg.user_from,
                    'username': sender_name
                    },
                'recipient': {
                    'id': msg.user_from,
                    'username': sender_name
                },
                'timestamp': msg.created_at.isoformat(),
                'is_own_message': bool
            },
            ...
        ]
     'is_mutual': bool
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


@socketio.on('connect', namespace='/chat')
def handle_chat_connect():
    # The SocketIO connection inherits the authentication state from HTTP client
    if not current_user.is_authenticated:
        print("Rejected unauthenticated connection")
        return False
    print(f"User {current_user.user_name} connected to chat namespace")
    return True

@socketio.on('join', namespace='/chat')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('room_joined', {'room': room})

# Handler for send events
@socketio.on('json', namespace='/chat')
def on_message(json):
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
        # print(f'Database error when saving message: {e}')
        db.rollback()
        emit('error', {'message': 'Failed to send message. Please try again.'}, broadcast=False)


# print(f"Decorator used socketio object: {socketio}")
# print(f"Socketio handlers after decoration: {socketio.handlers}")

# @socketio.on('connect')
# def handle_connect(message):
#     print('Client connected!')

# @socketio.on('message')
# def handle_message(message):
#     send(message, broadcast=True)
    
# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected!')

# # Saving a copy of the message to the database for the message history
# @socketio.on('database')
# def saveMessageToDb():    
#     #Parse and print inputs
#     msg = data.json['message']
#     sender = data.json['sender']
#     receiver = data.json['receiver']
#     now = datetime.datetime.now()
            
#     # Save message to database
#     print("Save to DB")
#     db = get_db()
#     db.execute("INSERT INTO message_data VALUES (?, ?, ?, ?)",
#                (sender, receiver, msg, now))
#     db.commit()
#     return

# # Get back the message history between two users
# @bp.route('/history', methods=['GET', 'POST'])
# def chatGetHistoryFromDb():
#     #Parse and print inputs
#     data = request.get_json(silent=True)
#     print("Request:" + str(data))
#     sender = data['sender']
#     receiver = data['receiver']
            
#     # Connect to DB and get history between two users (both message directions)
#     print("Retreive from DB")
#     db = get_db()
#     messages = db.execute("SELECT * FROM message_data WHERE \
#         (user_from = ? AND user_to = ?) OR \
#         (user_from = ? AND user_to = ?) ORDER BY created_at", 
#         (sender, receiver, receiver, sender)).fetchall()    
#     return messages
    