from flask import Blueprint, request, jsonify
from flask_login import login_required
from .db import get_db
from .data_classes import User
from sqlalchemy import select

bp = Blueprint('usersearch', __name__)

@bp.route('/users/search', methods=['GET'])
@login_required
def usersearch():
    # extract params from URL
    search_term = request.args.get('username', '')
    # query db for usernames
    db = get_db()
    # TO DO: add to db.py then import and call; should also be error handling here
    # since interacting with the database
    results = db.scalars(select(User).where(User.user_name.ilike(f"%{search_term}%"))).fetchall()
    results = [r.to_dict() for r in results]
    data = {}
    data['users'] = results
    if results:
        data['message'] = 'success'
    else:
        data['message'] = 'no results found'
    return jsonify(data), 200