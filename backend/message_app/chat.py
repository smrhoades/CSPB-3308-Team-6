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