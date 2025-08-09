from .data_classes import Base, Contact, User
from sqlalchemy import create_engine, select, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import click
from flask import g
from flask import current_app

from pathlib import Path

def get_db():
	if 'db' not in g:
		engine = current_app.engine
		Session = sessionmaker(bind=engine)
		g.db = Session()
	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_db():
	engine = current_app.engine
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

@click.command('init-db')
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo('Initialized the database.')

def init_app(app):
	path = app.config['DATABASE']
	app.engine = create_engine(f"sqlite:///{path}")
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	
def has_contact(session, user, contact):
	""" Checks if user has added contact """
	try:
		return session.scalar(
				select(
					exists().where(
						(Contact.user == user.id) &
						(Contact.contact == contact.id)
					)
				)
		)
	except SQLAlchemyError as e:
		print(f"Database error in has_contact: {e}")
		return False
		

def get_user_by_name(session, username):
	""" Returns User object of username if exists, else None """
	try:
		return session.scalar(select(User).where(User.user_name == username))
	except SQLAlchemyError as e:
		print(f'Database error in get_user_by_name: {e}')
		return None

def add_contact(session, user, contact):
	try:
		new_contact = Contact(user=user.id, contact=contact.id)
		session.add(new_contact)
		session.commit()
		return {'success': True, 'message': 'Contact added successfully'}
	except IntegrityError:
		session.rollback()
		return {'success': False, 'message': 'Database constraint violation'}
	except SQLAlchemyError as e:
		session.rollback()
		return {'success': False, 'message': f'Database error occurred: {e}'}
