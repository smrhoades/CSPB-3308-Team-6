import datetime

from flask import (
    Blueprint, g, jsonify, render_template, request
)
from message_app.db import get_db
from .__init__ import socketio

bp = Blueprint('chat', __name__)

# The template for the chat webpage
@bp.route('/chat')
def chat():
    print("Started page")
    return render_template('chat/chat.html')

@socketio.on('connect')
def handle_connect(message):
    print('Client connected!')

@socketio.on('message')
def handle_message(message):
    send(message, broadcast=True)
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

# Saving a copy of the message to the database for the message history
@socketio.on('database')
def saveMessageToDb():    
    #Parse and print inputs
    msg = data.json['message']
    sender = data.json['sender']
    receiver = data.json['receiver']
    now = datetime.datetime.now()
            
    # Save message to database
    print("Save to DB")
    db = get_db()
    db.execute("INSERT INTO message_data VALUES (?, ?, ?, ?)",
               (sender, receiver, msg, now))
    db.commit()
    return

# Get back the message history between two users
@bp.route('/history', methods=['GET', 'POST'])
def chatGetHistoryFromDb():
    #Parse and print inputs
    data = request.get_json(silent=True)
    print("Request:" + str(data))
    sender = data['sender']
    receiver = data['receiver']
            
    # Connect to DB and get history between two users (both message directions)
    print("Retreive from DB")
    db = get_db()
    messages = db.execute("SELECT * FROM message_data WHERE \
        (user_from = ? AND user_to = ?) OR \
        (user_from = ? AND user_to = ?) ORDER BY created_at", 
        (sender, receiver, receiver, sender)).fetchall()    
    return messages
    