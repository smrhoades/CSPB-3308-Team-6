from flask import Blueprint, jsonify
from message_app.db import get_db
from message_app.data_classes import User, Contact, Message
from sqlalchemy import select, or_, and_
from flask_login import login_required, current_user

bp = Blueprint('contacts', __name__)

@bp.route('/contacts', methods=['GET'])
@login_required
def contacts():
    # TO DO:
    # error handling
    # factor code blocks into functions and test
    user = current_user
    db = get_db()
    
    # Retrieve all contacts
    contacts_data = []
    query = select(Contact, User).join(User, Contact.contact == User.id).where(Contact.user == user.id)
    results = db.execute(query).all()
    for contact_row, user_row in results:
        contacts_data.append({
            'contact_id': contact_row.contact,
            'contact_name': user_row.user_name
        })

    # Retrieve three most recent messages
    query = select(Contact, User, Message).join(
        User, Contact.user == User.id
    ).join(
        Message, 
        or_(
            and_(Message.user_from == Contact.user, Message.user_to == Contact.contact),
            and_(Message.user_from == Contact.contact, Message.user_to == Contact.user)
        )
    ).where(Contact.user == current_user.id).order_by(Message.created_at.desc()).limit(3)
    results = db.execute(query).all()
    
    # Add current_user to contacts_data to simplify for loop
    contacts_data.append( {'contact_id': user.id, 'contact_name': user.user_name})
    contact_lookup = {contact['contact_id']: contact['contact_name'] for contact in contacts_data}

    message_data = []
    for contact_row, user_row, message_row in results:
        message_data.append(
            {
                'user_from_name': contact_lookup[message_row.user_from],
                'user_to_name': contact_lookup[message_row.user_to],
                'text': message_row.text,
                'created_at': message_row.created_at
            }
            )

    # remove current_user from contacts_data
    contacts_data.pop()

    return jsonify({'contacts_data': contacts_data, 'message_data': message_data})