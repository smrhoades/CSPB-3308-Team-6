from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from message_app.db import get_db
from message_app.data_classes import User, Contact, Message
from werkzeug.exceptions import abort
from .__init__ import socketio
from sqlalchemy import select, or_, func


bp = Blueprint('chat', __name__)

# The template for the chat webpage
@bp.route('/chat/<contact_uuid>', methods=['GET'])
@login_required
def chat(contact_uuid):
    db = get_db()
    
    # Check if contact exists
    contact_user = db.scalar(select(User).filter(User.uuid == contact_uuid))
    if not contact_user:
        abort(404)
        
    # Check if they have both added each other as contacts
    can_chat = db.execute(
        select(func.count())
        .select_from(Contact)
        .where(
            or_(
                (Contact.user == current_user.id) & (Contact.contact == contact_user.id),
                (Contact.user == contact_user.id) & (Contact.contact == current_user.id)
            )
        )
    ).scalar() == 2
    
    if not can_chat:
        abort(403)
    else:
        return jsonify({'status': 'success'})

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
    