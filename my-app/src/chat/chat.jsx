import './chat.css'
import { useState, useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useUser } from '../UserContext.jsx'

/*
Flow:
    - Fetch message history
    - Render message history
    - Emit Socket.IO connection request
    - Upon success, emit join room request
    - Emit send event every time "send" button is clicked
*/


// TODO:    
// Message data below will be sent from Flask
// Hardcoded for now

// const currentUser = 'Paul'
// const messagesData = [
// // id, user_from, user_to, text, created_at
//     [1, 'Paul', 'John', 'Good morning!', '10:15 AM'],
//     [2, 'John','Paul', 'How are you doing today?', '10:16 AM'],
//     [3, 'Paul', 'John', 'Feeling a bit under the weather actually. This message has to be particularly long though in order to test behavior of multi-line messages.', '10:21 AM'],
//     [4, 'John', 'Paul', 'Sorry to hear that', '10:22 PM'],
//     [5, 'John', 'Paul', 'This message is the first double text in the whole app.', '10:23 PM'],
//     [6, 'Paul', 'John', 'Lorem Ipsum and so on...', '11:30 PM'],
//     [7, 'Paul', 'John', 'zzzzz.....', '11:30 PM'],
//     [8, 'John', 'Paul', 'Maybe this message will make the conversation history long enough that it overflows the parent <div> element.', '11:31 PM'],
//     [9, 'Paul', 'John', 'It is!', '11:35 PM']
// ]

// fetches data, manages socket
function ChatContainer() {
    const [error, setError] = useState('')
    const [messagesLoading, setMessagesLoading] = useState(true);
    const [messagesData, setMessagesData] = useState([]);
    const { room_id } = useParams();
    const { user, isLoading } = useUser();

    const getMessageHistory = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/chat/${room_id}`,
                {
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                }
            );

            const messagesData = await response.json();
            console.log(messagesData.messages);
            setMessagesData(messagesData.messages);
        } catch (err) {
            setError("Couldn't retrieve message history:", error);
            return <div>{err}</div>
        } finally {
            setMessagesLoading(false);
        }
    };

    const sendHandler = () => 0; 

    useEffect(() => {
        getMessageHistory();
    }, [room_id]); // reload message history for different chats

   if (messagesLoading || isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <ChatInterface messagesData={messagesData} 
                       sendHandler={sendHandler} 
                       user={user}
                       error={error} />
    )
}

// renders everything
function ChatInterface({ messagesData, sendHandler, user, error }) {
    if (error) {
        return <div>{err}</div>;
    }
    else {
        return (
            <>
            <div className="center-box" id="outer-box">
                <h3>{user.username}'s conversation</h3>
                {
                    messagesData.map(({id, text, sender, recipient, timestamp}) => {
                        const msg_direction = sender.username === user.username ? 'to' : 'from'
                        return (
                        <div className={`chat-message-${msg_direction}`} key={id}>
                            {text}
                        </div>
                        )
                    })
                }
            </div>
            </>
        )
    }
}

export default ChatContainer

/* 
Refactored VisualMessagesList to separate data/state management and rendering. 

function VisualMessagesList() {
    const [error, setError] = useState('')
    const [messagesLoading, setMessagesLoading] = useState(true);
    const [messagesData, setMessagesData] = useState([]);
    const { room_id } = useParams();
    const { user, isLoading } = useUser();

    const getMessageHistory = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/chat/${room_id}`,
                {
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                }
            );

            const messagesData = await response.json();
            console.log(messagesData.messages);
            setMessagesData(messagesData.messages);
        } catch (err) {
            setError("Couldn't retrieve message history:", err);
        } finally {
            setMessagesLoading(false);
        }
    };

    useEffect(() => {
        getMessageHistory();
    }, [room_id]); // reload message history for different chats

   if (messagesLoading || isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <>
        <div className="center-box" id="outer-box">
            <h3>{user.username}'s conversation</h3>
            {
                messagesData.map(({id, text, sender, recipient, timestamp}) => {
                    const msg_direction = sender.username === user.username ? 'to' : 'from'
                    return (
                    <div className={`chat-message-${msg_direction}`} key={id}>
                        {text}
                    </div>
                    )
                })
            }

        </div>
        </>
    )
}

*/

            // <form id="message-input-form" onSubmit={(e) => {e.preventDefault(); handleSendMessage();}}>
            //     <input id="message-input" className="message-input" value={newMsg} onChange={(e) => setNewMsg(e.target.value)}></input>
            //     <button type="submit" onClick={handleSendMessage}>send</button>
            // </form>