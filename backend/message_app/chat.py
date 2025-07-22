from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from message_app.db import get_db
from message_app.data_classes import User, Contact, Message
from werkzeug.exceptions import abort
from message_app import socketio
from sqlalchemy import select, exists, func, or_
from flask_socketio import join_room, emit


bp = Blueprint('chat', __name__)

# Page load and authentication
@bp.route('/chat/<contact_uuid>', methods=['GET'])
@login_required
def chat(contact_uuid):
    db = get_db()
    
    # Check if contact exists
    contact_user = db.scalar(select(User).filter(User.uuid == contact_uuid))
    if not contact_user:
        abort(404)
        
    # Check if user has added contact to contacts
    can_chat = db.scalar(
        select(
            exists().where(
                (Contact.user == current_user.id) &
                (Contact.contact == contact_user.id)
                )
            )
        )
    
    if not can_chat:
        abort(403)
    else:
        return jsonify({'status': 'success'})

# Message history API
@bp.route('/chat/<contact_uuid>/messages', methods=['GET'])
@login_required
def get_chat_messages(contact_uuid):
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
    
    contact_user = db.scalar(select(User).filter(User.uuid == contact_uuid))
    if not contact_user:
        abort(404)

    messages = db.execute(
        select(
            Message,
            User.user_name.label('sender_name')
            )
            .join(User, Message.user_from == User.id)
            .where(
                or_(
                    (Message.user_from == current_user.id) & (Message.user_to == contact_user.id),
                    (Message.user_from == contact_user.id) & (Message.user_to == current_user.id)
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
                (Contact.user == current_user.id) & (Contact.contact == contact_user.id),
                (Contact.user == contact_user.id) & (Contact.contact == current_user.id)
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
    