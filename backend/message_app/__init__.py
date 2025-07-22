import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_login import LoginManager
from message_app.prefix import PrefixMiddleware

from sqlalchemy import select

# Create instance of SocketIO: not yet bound to any Flask app
# server attribute is None b/c there is no app to serve
socketio = SocketIO(logger=True, engineio_logger=True)
print(f"SocketIO created at module level: {socketio}")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    print(f"Flask app created: {hex(id(app))} ")
    # Bind SocketIO instance to our app
    #   - register SocketIO handlers with our app
    #   - set up necessary routes for WebSocket connections
    #   - does NOT start the server: SocketIO is configured but not running
    socketio.init_app(app)
    print(f"SocketIO object initialized in create_app(): {app.extensions['socketio']}")

    PrefixMiddleware(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'messenger.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Allow requests from React
    CORS(app, origins=["http://localhost:5173"])
    # print("CORS configured")

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        from .data_classes import User
        from .db import get_db
        db = get_db()
        return db.scalar(select(User).where(User.id == int(user_id)))


    print("App config" + str(app.config))

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import contacts
    app.register_blueprint(contacts.bp)

    from . import chat
    app.register_blueprint(chat.bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Starts server that can handle BOTH HTTP requests and WebSocket connections
    #  - sets socketio.server
    #  - begins listening for connections
    #  - blocks and runs the event loop
    socketio.run(app)
