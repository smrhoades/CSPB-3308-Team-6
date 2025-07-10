import datetime

from flask import (
    Blueprint, g, render_template
)
from message_app.db import get_db
from .__init__ import socketio

bp = Blueprint('chat', __name__)

# The template for the chat webpage
@bp.route('/chat')
def chat():
    print("Started page")
    return render_template('chat/chat.html')

# Saving a copy of the message to the database for the message history
@socketio.on('database')
def saveMessageToDb():
    print('received message: ' + data)
    db = get_db()
    
    msg = data.json['message']
    sender = data.json['sender']
    receiver = data.json['receiver']
    now = datetime.datetime.now()
            
    print("Save to DB")
    db.execute("INSERT INTO message_data VALUES (?, ?, ?, ?)",
               (sender, receiver, msg, now))
    db.commit()
    return