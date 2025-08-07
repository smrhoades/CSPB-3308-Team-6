import './chat.css'
import { useState, useEffect, useRef } from 'react'
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
    const messagesEndRef = useRef(null);
    const textareaRef = useRef(null);
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

    useEffect(() => {
        // When messages change, scroll to bottom
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollTop = messagesEndRef.current.scrollHeight;
        }
    }, [messages]);

    const resizeTextarea = () => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto'; // Reset to measure content
            const scrollHeight = textareaRef.current.scrollHeight;

            // Set limits
            const newHeight = Math.min(scrollHeight, 60);
            textareaRef.current.style.height = newHeight + 'px';
        }
    }

    return (
        <>
        <div className="chat-container" id="chat-outer-box">
            <div className="chat-header"><h3>Conversation with {contactUsername}</h3></div>
            <div className="messages" ref={messagesEndRef}>
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
            </div>
            <div className="input-container">
                <textarea id="input-box"
                    ref={textareaRef}
                    value={text}
                    onChange={(e) => { setText(e.target.value); resizeTextarea() }}
                    onKeyDown={(e) => e.key === 'Enter' && sendHandler(contactUsername, text)}
                />
                <button type="button" onClick={(event) => sendHandler(contactUsername, text)}>send</button>
            </div>
        </div>
        </>
    )
}

export default ChatContainer