import './chat.css'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

// TODO:    
// Message data below will be sent from Flask
// Hardcoded for now

const currentUser = 'Paul'
const messagesData = [
// id, user_from, user_to, text, created_at
    [1, 'Paul', 'John', 'Good morning!', '10:15 AM'],
    [2, 'John','Paul', 'How are you doing today?', '10:16 AM'],
    [3, 'Paul', 'John', 'Feeling a bit under the weather actually. This message has to be particularly long though in order to test behavior of multi-line messages.', '10:21 AM'],
    [4, 'John', 'Paul', 'Sorry to hear that', '10:22 PM'],
    [5, 'John', 'Paul', 'This message is the first double text in the whole app.', '10:23 PM'],
    [6, 'Paul', 'John', 'Lorem Ipsum and so on...', '11:30 PM'],
    [7, 'Paul', 'John', 'zzzzz.....', '11:30 PM'],
    [8, 'John', 'Paul', 'Maybe this message will make the conversation history long enough that it overflows the parent <div> element.', '11:31 PM'],
    [9, 'Paul', 'John', 'It is!', '11:35 PM']
]



function VisualMessagesList({ conversation, user }) {
    const [newMsg, setNewMsg] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleSendMessage = async () => {
        const requestBody = JSON.stringify({newMsg})
        console.log(requestBody) // for testing
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', //placeholder
                {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: requestBody
                }
            );

            const data = await response.json()
            console.log(data) // for testing

            if (data.status === 'success') {
                navigate('/chat') // one way to refresh the page...
            } else {
                setError(`Message Send error with msg: ${data.message}`)
                console.log(data)
            }
        } catch (err) {
            setError('Server Error: no response from Flask')
        }
        setNewMsg('')
    };

    return (
        <>
            {
                conversation.map(([id, user_from, user_to, text, created_at]) => {
                    const msg_direction = user_from === user ? 'to' : 'from'
                    return (
                    <div className={`chat-message-${msg_direction}`} key={id}>
                        {text}
                    </div>
                    )
                })
            }
            <form id="message-input-form" onSubmit={(e) => {e.preventDefault(); handleSendMessage();}}>
                <input id="message-input" className="message-input" value={newMsg} onChange={(e) => setNewMsg(e.target.value)}></input>
                <button type="submit" onClick={handleSendMessage}>send</button>
            </form>
        </>
    )
}

export default VisualMessagesList

/*
TODO:
wide message box right aligned at bottom with "send" button
clicking send sends a json to flask and console.log()s it for verification
add link to contact page

Cut out chat from contacts page
add text input for adding a contact
clicking "add" button sends a json to flask
*/