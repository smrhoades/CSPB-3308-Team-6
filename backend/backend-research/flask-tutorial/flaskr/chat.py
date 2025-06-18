from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_socketio import send, emit


from .__init__ import socketio

bp = Blueprint('chat', __name__)

@bp.route('/chat')
def chat():
    return render_template('chat/chat.html')

@socketio.on('connection event')
def handle_my_custom_event(message):
    print(message['data'])

@socketio.on('message')
def handle_message(message):
    send(message, broadcast=True)
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')