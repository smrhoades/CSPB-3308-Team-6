from message_app.data_classes import User, Contact, Message
from message_app.db import get_db
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

def create_test_datetime(year=2024, month=1, day=1, hour=1, minute=1, second=0):
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)

def insert_user_data():
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
    
    test_user_island = User(
        user_name = 'island',
        user_pwd = generate_password_hash('island')
    )

    db = get_db()
    db.add(test_user)
    db.add(other_user)
    db.add(test_user2)
    db.add(test_user_island)
    db.commit()
    
def insert_contact_data():
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
        text = "message from test to other",
        created_at = create_test_datetime(year=2024, month=1, day=1, hour=1, minute=0, second=0)
    )
    
    test_other_message_to_user = Message(
        user_from = 2,
        user_to = 1,
        text = "message from other to test",
        created_at = create_test_datetime(year=2025, month=1, day=2, hour=1, minute=0, second=0)
    )
    
    test_user_message_to_test2 = Message(
        user_from = 1,
        user_to = 3,
        text = "message from test to test2",
        created_at = create_test_datetime(year=2025, month=1, day=3, hour=1, minute=0, second=0)
    )
    
    test_test2_message_to_test = Message(
        user_from = 3,
        user_to = 1,
        text = "message from test2 to test",
        created_at = create_test_datetime(year=2025, month=1, day=4, hour=1, minute=0, second=0)
    )

    db = get_db()
    db.add(test_user_message_to_other)
    db.add(test_other_message_to_user)
    db.add(test_user_message_to_test2)
    db.add(test_test2_message_to_test)
    db.commit()
    
def insert_test_data():
    insert_user_data()
    insert_contact_data()
    insert_message_data()