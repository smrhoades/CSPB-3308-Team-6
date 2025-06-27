from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from message_app.auth import login_required
from message_app.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('home/home.html')