from .data_classes import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
	# path = current_app.config['DATABASE']
	# engine = create_engine(f"sqlite:///messenger.db")
	# print(f"Initializing DB to {path}")
	# engine = create_engine(f"sqlite:///{path}")
	# print(f"Initialized DB to {path}")
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
