Chat page testing/functionality requirements

URL Structure:
- '/chat/{contact_user_id}' where contact_user_id is the UUID of the user being chatted with √

Page Load ('/chat/{contact_user_id}'):
- Verify user has permission to chat with this contact (check contacts table) √
- Load chat history (messages between current user and contact_user_id) √
- Sort messages chronologically √
- WebSocket connection opened with room = deterministic chat room name
    - Open WebSocket connection √
    - Join a "room" for this specific conversation √

Message Sending:
- Validate message content (non-empty, length limits)
- Store message in database immediately (commit transaction) √
- On successful DB write: broadcast to WebSocket room √
- On DB failure: send error response to sender
- Include timestamp and sender info in broadcast √

Message Receiving (via WebSocket):
- Display message in chat interface
- Update UI to show message as delivered

Page Leave:
- WebSocket connection closed
- Clean up any pending message states

Error Handling:
- Handle WebSocket disconnections/reconnections
- Handle database write failures
- Handle invalid contact_user_id (404 or redirect)

Testing Scenarios to Consider
- User tries to access chat with non-contact
- WebSocket connection drops mid-conversation
- Multiple messages sent rapidly
- Very long messages
- Special characters/emojis in messages
- User opens multiple chat windows