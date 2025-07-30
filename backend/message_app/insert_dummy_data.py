from data_classes import User, Contact, Message
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime, timezone

"""
    Inserts test data into database.
"""

def create_test_datetime(year=2024, month=1, day=1, hour=1, minute=1, second=0):
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)

path = '../instance/messenger.db'
engine = create_engine(f"sqlite:///{path}")
# engine = create_engine(f"sqlite:///{path}", echo=True)

u1 = User(
    user_name = 'test',
    user_pwd = 'test'
)

u2 = User(
    user_name = 'test2',
    user_pwd = 'test2'
)

tm1 = Message(
    user_from = 1,
    user_to = 2,
    text = "Hello from test user!",
    created_at = create_test_datetime(year=2025, month=1, day=1, hour=1, minute=0, second=0)
)

tm2 = Message(
    user_from = 2,
    user_to = 1,
    text = "Hello back from test2!",
    created_at = create_test_datetime(year=2025, month=1, day=2, hour=1, minute=0, second=0)
)
# Long message
tm3 = Message(
    user_from = 1,
    user_to = 2,
    text = "long message " * 20,
    created_at = create_test_datetime(year=2025, month=1, day=5, hour=1, minute=0, second=0)
)

c1 = Contact(
    user = 1,
    contact = 2
)

c2 = Contact(
    user = 2,
    contact = 1,
)

with Session(engine) as session:
        try:
            session.add_all([u1, u2, tm1, tm2, tm3, c1, c2])

            session.commit()
            result = session.execute(select(User)).fetchall()
            print("Retrieved users:", [r[0].user_name for r in result])
            
            result = session.execute(select(Message)).fetchall()
            print("Retrieved messages:", [m[0].text for m in result])
            
            result = session.execute(select(Contact)).fetchall()
            print("Retrieved contacts:", [(c[0].user, c[0].contact) for c in result])
            
        except:
            session.rollback()
            print("Unable to add data: probably the data already exists in the db")
            print("Try re-initializing the db")