from flask import Blueprint, jsonify, request
from message_app.db import get_db, get_user_by_name, has_contact, add_contact
from message_app.data_classes import User, Contact, Message
from sqlalchemy import select, or_, and_
from flask_login import login_required, current_user

bp = Blueprint('contacts', __name__)

@bp.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    # TO DO:
    # error handling
    # factor code blocks into functions and test
    if request.method == 'GET':
        user = current_user
        db = get_db()
        
        # Retrieve all contacts
        # TO DO: make this a db.py function then import and call
        # Furthermore, should just return the User object for each contact
        contacts_data = []
        query = select(Contact, User).join(User, Contact.contact == User.id).where(Contact.user == user.id)
        results = db.execute(query).all()
        for contact_row, user_row in results:
            contacts_data.append({
                'contact_id': contact_row.contact,
                'contact_name': user_row.user_name,
                'contact_uuid': user_row.uuid
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

        return jsonify({'contacts_data': contacts_data, 'message_data': message_data}), 200
    
    elif request.method == 'POST':
        data = {} # return container
        username = request.json['username']
        
        # validate user is not adding themselves
        if username == current_user.user_name:
            data['message'] = 'cannot add self as a contact'
            return jsonify(data), 200
        
        db = get_db()

        # validate user exists
        contact = get_user_by_name(db, username)
        if not contact:
            data['message'] = f'user {username} not found'
            return jsonify(data), 200

        # validate user is not already in current user's contacts
        if has_contact(db, current_user, contact):
            data['message'] = f'{username} already in contacts'
            return jsonify(data), 200
        
        # update database with new contact
        result = add_contact(db, current_user, contact)
        if result['success'] == True:
            data['message'] = 'success'
            return jsonify(data), 200
        else:
            data['message'] = result['message']
            return jsonify(data), 200