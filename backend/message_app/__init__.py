import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from message_app.prefix import PrefixMiddleware

socketio = SocketIO(logger=True, engineio_logger=True)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    PrefixMiddleware(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'messenger.db'),
    )

    # Allow requests from React
    CORS(app, origins=["http://localhost:5173"])
    print("CORS configured")

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
    
    print("App config" + str(app.config))

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
   
    # socketio 
    socketio.init_app(app)

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
    socketio.run(app)
