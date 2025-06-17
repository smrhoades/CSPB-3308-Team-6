from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_socketio import send, emit


from .__init__ import socketio

bp = Blueprint('chat', __name__)

@bp.route('/chat')
def chat():
    return render_template('chat/chat.html')

@socketio.on('my event')
def handle_my_custom_event(json):
    print('connected')

@socketio.on('message')
def handle_message(message):
    send(message, broadcast=True)

