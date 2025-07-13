from .data_classes import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import click
from flask import g

def get_db():
	if 'db' not in g:
		engine = create_engine("sqlite:///messenger.db")
		Session = sessionmaker(bind=engine)
		g.db = Session()
	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_db():
	engine = create_engine("sqlite:///messenger.db")
	# initialize clean database each time
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
		
@click.command('init-db')
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo('Initialized the database.')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
