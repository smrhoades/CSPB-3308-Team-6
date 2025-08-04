# Notes on the back-and-forth between Client and Server for chatting.

PROPOSED CHANGE:
- the URL for conversations should be changed to 'chat/<room_id>' so that links can be bookmarked and shared. Currently the URL is 'chat/<contact_uuid>', so if User A shares the link with User B, User B will get a link to a conversation with themselves, which will result in a 403 error. 

NOTE: 
How 'room_id' is currently generated: 
```min('user1_uuid+user2_uuid', 'user2_uuid+user1_uuid')```

### Opening the chat page
1. User wants to open conversation with contact, so they click on the contact's user_name on their '/contacts' page. 
1. Client requests '/chat/<room_id>' endpoint from Server.
1. Server authenticates request and serves message history to Client. 
1. Client requests a WebSocket connection.
1. Server authenticates request.
1. Client requests to "join", including the room_id in the request.
1. Server puts client in the room (which may or may not be empty) and emits confirmation message. 
1. Client's browser renders conversation page on '/chat/<room_id>'.

### Chatting 
1. User sends a message by clicking "send" button.
1. Client sends WebSocket event with JSON data:
	{
	 'recipient_user_name': ...,
	 'message': ...
	}
1. Server receives data, stores message in database, appends retrieved fields to received data, and sends WebSocket event with data to everyone in the room:
	{
	 'recipient_user_name': ...,
	 'message': ...,
	 'sender': ...,
	 'created_at': ...
	}
1. Client receives event, renders data in the browser. 

### Disconnecting
1. When User navigates away, WebSocket connection automatically disconnects.