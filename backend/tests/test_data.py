from message_app.data_classes import User
from message_app.db import get_db

def insert_test_data():
    db = get_db()
    
    # Create test users
    test_user = User(
        user_name = 'test',
        user_pwd = 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'
    )
    other_user = User(
        user_name = 'other',
        user_pwd = 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'
    )
    
    db.add(test_user)
    db.add(other_user)
    db.commit()