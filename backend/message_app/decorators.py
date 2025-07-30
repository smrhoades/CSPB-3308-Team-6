from functools import wraps
from flask import abort
from flask_login import current_user
from .data_classes import User, Contact
from .db import get_db
from sqlalchemy import select, exists

def parse_room_id(room_id):
    print("room_id is:", room_id)
    """ parses a room_id to and returns a tuple with current_user.uuid first """
    if room_id[:len(current_user.uuid)] == current_user.uuid:
        return current_user.uuid, room_id[len(current_user.uuid):]
    else:
        return current_user.uuid, room_id[:len(current_user.uuid)]

def contact_required(f):
    @wraps(f)
    def decorated_function(room_id, *args, **kwargs):
        db = get_db()

        _, contact_uuid = parse_room_id(room_id)
        # Check if contact exists
        contact = db.scalar(select(User).filter(User.uuid==contact_uuid))
        if not contact:
            abort(404)
            
        # Check if current user has added this contact
        can_chat = db.scalar(
            select(
                exists().where(
                    Contact.user == current_user.id) &
                    (Contact.contact == contact.id)
                )
            )

        if not can_chat:
            abort(403) # or redirect to contact page
            
        return f(contact_uuid, contact, *args, **kwargs)
    return decorated_function