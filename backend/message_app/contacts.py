from flask import Blueprint, g
from message_app.db import get_db
from message_app.data_classes import User, Contact, Message
from sqlalchemy import select, where, or_, and_

bp = Blueprint('contacts', __name__)

@bp.route('/contacts', methods=['GET'])
def contacts():
    user = g.user
    db = get_db()
    
    contacts_data = []
    query = select(Contact, User).join(User, Contact.contact == User.id).where(Contact.user == user.id)
    results = db.execute(query).all()
    for contact_row, user_row in results:
        contacts_data.append({
            'contact_id': contact_row.contact,
            'contact_name': user_row.user_name
        })
        
    recents = [] # list of Message objects
    for contact in contacts:
        stmt = select(Message).where(
            or_(
                and_(Message.user_from==1, Message.user_to==contact.contact),
                and_(Message.user_from==contact.contact, Message.user_to==1)
            )
        ).order_by(Message.created_at.desc())
        recent_message = db.scalars(stmt).first()
        if recent_message:
            recents.append(recent_message)