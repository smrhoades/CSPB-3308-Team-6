import sqlite3
from werkzeug.security import generate_password_hash

username1 = 'test'
password1 = generate_password_hash('test')

conn = sqlite3.connect('messenger_app.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE user(id INTEGER, username TEXT, password TEXT)")
c.execute("INSERT INTO user VALUES (?, ?, ?)", (1, username1, password1))
conn.commit()
conn.close()
