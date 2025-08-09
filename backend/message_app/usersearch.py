from flask import Blueprint, request, make_response, jsonify
from flask_login import login_required
from .db import get_db
from .data_classes import User
from sqlalchemy import select

bp = Blueprint('usersearch', __name__)

@bp.route('/users/search', methods=['GET'])
@login_required
def usersearch():
    # extract params from URL
    search_term = request.args.get('user', '')
    # query db for usernames
    db = get_db()
    results = db.scalars(select(User.user_name).where(User.user_name.ilike(f"%{search_term}%"))).fetchall()
    # print("retrieved", results)
    data = {}
    if results:
        data['status'] = 'success'
        data['usernames'] = results
        return jsonify(data), 200
    else:
        data['status'] = 'error'
        data['message'] = 'no results found'
        return jsonify(data), 200