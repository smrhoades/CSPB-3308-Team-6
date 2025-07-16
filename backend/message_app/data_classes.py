from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime, func
from flask_login import UserMixin
import uuid

class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = 'user_data'
    id = Column(Integer, primary_key=True, autoincrement=True) # Faster for JOINs
    uuid = Column(String, unique=True, default=lambda: str(uuid.uuid4())) # For URLs
    user_name = Column(String, unique=True, nullable=False)
    user_pwd = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    modified_at = Column(DateTime(timezone=True), default=func.now())

class Message(Base):
    __tablename__ = 'message_data'
    id = Column(Integer, primary_key=True)
    user_from = Column(ForeignKey('user_data.id', ondelete='CASCADE'))
    user_to = Column(ForeignKey('user_data.id', ondelete='CASCADE'))
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Contact(Base):
    __tablename__ = 'contacts'
    __table_args__ = (UniqueConstraint('user', 'contact'),)
    
    id = Column(Integer, primary_key=True)
    user = Column(ForeignKey('user_data.id', ondelete='CASCADE'))
    contact = Column(ForeignKey('user_data.id', ondelete='CASCADE'))