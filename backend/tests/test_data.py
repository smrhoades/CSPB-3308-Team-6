from message_app.data_classes import User, Contact, Message
from message_app.db import get_db
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone



def insert_test_data():
    # Create test users
    test_user = User(
        user_name = 'test',
        user_pwd = 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'
    )

    other_user = User(
        user_name = 'other',
        user_pwd = 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'
    )

    test_user2 = User(
        user_name = 'test2',
        user_pwd =  generate_password_hash('test2')
    )

    db = get_db()
    db.add(test_user)
    db.add(other_user)
    db.add(test_user2)
    db.commit()
    
def insert_test_contact_data():
    """
    test_user is friends with everyone
    other_user and test_user2 are not friends with each other
    """
    test_user_contact1 = Contact(
        user = 1,
        contact = 2
    )
    
    test_user_contact2 = Contact(
        user = 1,
        contact = 3    
    )
    
    other_user_contact = Contact(
        user = 2,
        contact = 1,
    )

    test_user2_contact = Contact(
        user = 3,
        contact = 1    
    )
    
    db = get_db()
    db.add(test_user_contact1)
    db.add(test_user_contact2)
    db.add(other_user_contact)
    db.add(test_user2_contact)
    db.commit()
    
def insert_message_data():
    test_user_message_to_other = Message(
        user_from = 1,
        user_to = 2,
        text = "test message 1",
        created_at = datetime(2025, 1, 14, 10, 30, 0, tzinfo=timezone.utc) # 2025-01-14 10:30:00+00:00
    )
    
    test_other_message_to_user = Message(
        user_from = 2,
        user_to = 1,
        text = "test message 2",
        created_at = datetime(2025, 1, 15, 10, 30, 0, tzinfo=timezone.utc) # 2025-01-15 10:30:00+00:00
    )
    
    db = get_db()
    db.add(test_user_message_to_other)
    db.add(test_other_message_to_user)
    db.commit()