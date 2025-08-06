import './chat.css'
import { useState, useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useUser } from '../UserContext.jsx'
import { useSocket } from '../SocketioContext.jsx'

/*
Flow:
    - Fetch message history
    - Render message history
    - Emit Socket.IO connection request
    - Upon success, emit join room request
    - Emit send event every time "send" button is clicked
*/

// fetches data, manages socket
function ChatContainer() {
    const [error, setError] = useState('')
    const [messagesLoading, setMessagesLoading] = useState(true);
    const [messages, setMessages] = useState([]);
    const { roomId } = useParams();
    const { user, isLoading } = useUser();
    const { joinRoom, sendMessage, subscribeToRoom } = useSocket();

    const getMessageHistory = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/chat/${roomId}`,
                {
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                }
            );

            const messagesData = await response.json();
            setMessages(messagesData.messages);
        } catch (error) {
            setError("Couldn't retrieve message history:", error);
        } finally {
            setMessagesLoading(false);
        }
    };

    useEffect(() => {
        getMessageHistory();
        joinRoom(roomId);
        const unsubscribe = subscribeToRoom(roomId, (newMessage) => {
            setMessages(prev => [...prev, newMessage]);
        });

        return unsubscribe;        // Clean up
    }, [roomId, subscribeToRoom]); // reload message history for different chats

   if (messagesLoading || isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ChatInterface messages={messages} 
                       sendMessage={sendMessage} 
                       user={user}
                       error={error} />
    )
}

// renders everything
function ChatInterface({ messages, sendMessage, user, error }) {
    if (error) {
        return <div>{error}</div>;
    }
    const [text, setText] = useState('');
    const sendHandler = (to, msg) => {
        if (msg !== '') {
            sendMessage(to, msg);
            setText('');
        }
    }
    var contactUsername = 'Loading...';
    if (messages.length > 0) {
        contactUsername = messages[0].sender.username == user.username ? messages[0].recipient.username : messages[0].sender.username;
    }
    return (
        <>
        <div className="center-box" id="outer-box">
            <h3>{user.username}'s conversation with {contactUsername}</h3>
            {
                messages.map(({id, text, sender, recipient, timestamp}) => {
                    const msg_direction = sender.username === user.username ? 'to' : 'from'
                    return (
                    <div className={`chat-message-${msg_direction}`} key={id}>
                        {text}
                    </div>
                    )
                })
            }
            <input
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendHandler(contactUsername, text)}
            />
            <button type="button" onClick={(event) => sendHandler(contactUsername, text)}>send</button>
        </div>
        </>
    )
}

export default ChatContainer