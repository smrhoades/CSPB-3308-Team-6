import './contacts-list.css'

// TODO:    
// Message data below will be sent from Flask
// Hardcoded for now
const contactsArray = ['John','Paul','George','Ringo'];
const messagesData = {
    'John': [
        { direction: 'to',   time: '10:15 AM', text: 'Good morning!' },
        { direction: 'from', time: '10:16 AM', text: 'Good morning! How are you doing today?' },
        { direction: 'to',   time: '10:21 AM', text: 'Feeling a bit under the weather actually. This message has to be particularly long though in order to test behavior of multi-line messages.' },
        { direction: 'from', time: '10:22 AM', text: 'Sorry to hear that.' }
    ]
}

function VisualContactsList({ contacts }) {
    return (
            <>
                {
                    contacts.map((contactName, index) => (
                        <div className="contact-card" key={index}>{contactName}</div>
                    ))
                }
            </>
    )
}

function VisualMessagesList({ conversation }) {
    return (
        <>
            {
                conversation.map((msg, index) => (
                        <div className={`chat-message-${msg.direction}`} key={index}>
                            {msg.text}
                        </div>
                ))
            }
        </>
    )
}

function ContactsList() {

    return (
        <div className="center-box" id="outer-box">
            <div id="inner-box">
                <div id="contacts-box">
                    <h1>Contacts</h1>
                    <VisualContactsList contacts={contactsArray}/>
                </div>
                <div id="chat-outer-box">
                    <h1>John</h1>
                    <VisualMessagesList conversation={messagesData.John}/>
                </div>
            </div>
        </div>
    )
}

export default ContactsList