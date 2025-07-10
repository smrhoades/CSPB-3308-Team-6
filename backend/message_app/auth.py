from flask import (
	Blueprint, g, request, session, make_response
)
from http import HTTPStatus
from werkzeug.security import check_password_hash, generate_password_hash

from message_app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
	username = request.json['username']
	password = request.json['password']
	db = get_db()
	error = None

	# TO DO: React should ensure that empty username and passwords aren't sent?
	if not username:
		error = 'Username is required.'
	elif not password:
		error = 'Password is required.'

	if error is None:
		try:
			db.execute(
				"INSERT INTO user (username, password) VALUES (?, ?)",
				(username, generate_password_hash(password)),
			)
			db.commit()
			data = {'status': 'success'}
			return make_response(data)
		
		except db.IntegrityError:
			# Undo changes so that db gets back to consistent state
			db.rollback()
			error = f"User {username} is already registered."
			data = {'error': error}
			# send 409 status code
			return make_response(data, HTTPStatus.CONFLICT)
			
	else:
			# This is unnecessary IF React ensures empty usernames/passwords aren't sent
			data = {'error': error}
			return make_response(data)

@bp.route('/login', methods=['POST'])
def login():
	username = request.json['username']
	password = request.json['password']
	db = get_db()
	error = None
	user = db.execute(
		'SELECT * FROM user WHERE username = ?', (username,)
	).fetchone()

	if user is None:
		error = 'Incorrect username.'
		data = {'error': error}
		return make_response(data, HTTPStatus.CONFLICT)
	elif not check_password_hash(user['password'], password):
		error = 'Incorrect password.'
		data = {'error': error}
		return make_response(data, HTTPStatus.CONFLICT)

	if error is None:
		session.clear()
		session['user_id'] = user['id']
		data = {'status': 'success'}
		return make_response(data)

@bp.before_app_request
def load_logged_in_usr():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	data = {'status': 'success'}
	return make_response(data)



