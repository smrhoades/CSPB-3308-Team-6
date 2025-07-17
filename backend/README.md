### Routes

The following routes are functioning:
- /auth/register
- /auth/login
- /contacts

Under development:
- /chat/{contact_uuid}

To do:
- /profile
- /add_contact

### Running and Testing

All of the following commands should be run while in the ```backend``` folder.

Before starting up the server you must initialize the database. Do so with
```flask --app message_app init-db```

If you commit anything to the database, you can clear it by running the command again. 

To start the server, do
```python3 run.py```

To run the tests, do
```pytest```

You can run specific tests with, e.g,
```pytest tests/test_contacts.py```