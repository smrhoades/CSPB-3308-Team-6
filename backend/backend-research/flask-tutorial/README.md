
Links to tutorials:

https://flask.palletsprojects.com/en/stable/tutorial/

https://flask-socketio.readthedocs.io/en/latest/getting_started.html

It looks like in Week 6 we're doing a flask tutorial as a lab, so it's probably better to just do that instead of the 'official' tutorial. However, the bit about flask-socketio will be unique to our application since that's how flask sets up WebSockets (see below), so if you're comfortable with basic backend stuff have a look at that.  

Installations:
- pip install Flask
- pip install flask-socketio

It's a good idea to set up a virtual environment. [This link] (https://flask.palletsprojects.com/en/stable/installation/) shows how. 

First time around you need to initialize the database (for the blog part of the tutorial, which I kept in this prototype since it implements login/authorization):
```flask --app flaskr init_db```

After that you do
```python run.py```

to start a server. 

Now you can go to http://127.0.0.1:5000 to see the index.html page for the normal Flask tutorial, which is a blog website. You can register and login with test credentials. You test out the create/edit buttons. 

To access the chat page go to http://127.0.0.1:5000/chat. (There's no link to it from the blog page itself.)

Open up another window and go to the same URL and you'll see that when you enter text, it shows up in both windows instantly.

### WebSockets ###
This was a cool thing I learned about this week and it's an essential concept on the backend, so I'm writing up a brief explainer here. If you have more to add, or corrections to what I say, don't hesitate to bring them up. 

In a traditional client-server connection (HTTP), the client sends a request to a server, the server handles the request (say by retrieving data and sending it back to the client) and then the connection is closed. In this way, the server is always passive, waiting for requests from the client. We _could_ build a messaging app that works with this model, but the browser would have to automatically send a request to the server maybe once or twice a second (to avoid the need for the user to refresh the page: this is called _polling_), but it would be better if we could just keep the connection open instead of closing it after one request.

WebSockets does just that. It's a communication protocol that keeps a connection between client and server open indefinitely. With a persistent connection, the server can now push data to the client without having to wait for a request (b/c a request is the only way a connection is established in HTTP). This is what we want for a messaging app, because it's how we get a message to pop up in the browser in real time. 

https://www.geeksforgeeks.org/what-is-web-socket-and-how-it-is-different-from-the-http/