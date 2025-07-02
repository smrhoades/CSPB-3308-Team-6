from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_socketio import send, emit

from .__init__ import socketio

bp = Blueprint('chat', __name__)

# The template for the chat webpage
@bp.route('/chat')
def chat():
    print("Started page")
    return render_template('chat/chat.html')

# Handles client connects
# TODO, not actually sure this is run over chat.html
@socketio.on('connection event')
def handle_my_custom_event(message):
    print(message['data'])

# Runs when the user clicks the 'Send' button
# TODO, not actually sure this is run over chat.html
@socketio.on('message')
def handle_message(message):
    send(message, broadcast=True)
    
# Handles client diconnects
# TODO, not actually sure this is run over chat.html
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

# Handles errors in the chat rooms
# TODO, not actually sure this is run over chat.html
@socketio.on_error('/chat') # handles the '/chat' namespace only
def error_handler_chat(e):
    pass
