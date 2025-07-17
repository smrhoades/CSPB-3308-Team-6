from message_app.__init__ import create_app, socketio

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)
