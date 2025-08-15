from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime, func
from flask_login import UserMixin
import uuid

from . import db_

class User(db_.Model, UserMixin):
    __tablename__ = 'user_data'
    id = db_.Column(db_.Integer, primary_key=True, autoincrement=True) # Faster for JOINs
    uuid = db_.Column(db_.String, unique=True, default=lambda: str(uuid.uuid4())) # For URLs
    user_name = db_.Column(db_.String, unique=True, nullable=False)
    user_pwd = db_.Column(db_.String, nullable=False)
    created_at = db_.Column(db_.DateTime(timezone=True), default=func.now())
    modified_at = db_.Column(db_.DateTime(timezone=True), default=func.now())
    
    def to_dict(self):
        return {'id': self.id, 'uuid': self.uuid, 'user_name': self.user_name,
                'user_pwd': self.user_pwd, 'created_at': self.created_at,
                'modified_at': self.modified_at}

class Message(db_.Model):
    __tablename__ = 'message_data'
    id = db_.Column(db_.Integer, primary_key=True)
    user_from = db_.Column(db_.ForeignKey('user_data.id', ondelete='CASCADE'))
    user_to = db_.Column(db_.ForeignKey('user_data.id', ondelete='CASCADE'))
    text = db_.Column(db_.String, nullable=False)
    created_at = db_.Column(db_.DateTime(timezone=True), default=func.now())

class Contact(db_.Model):
    __tablename__ = 'contacts'
    __table_args__ = (db_.UniqueConstraint('user', 'contact'),)
    
    id = db_.Column(db_.Integer, primary_key=True)
    user = db_.Column(db_.ForeignKey('user_data.id', ondelete='CASCADE'))
    contact = db_.Column(db_.ForeignKey('user_data.id', ondelete='CASCADE'))