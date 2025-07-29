import './contacts.css'

const contactsArray = ['John','Paul','George','Ringo'];

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


function ContactsList() {

    return (
        <div className="center-box" id="outer-box">
            <h1>Contacts</h1>
            <VisualContactsList contacts={contactsArray}/>
        </div>
    )
}

export default ContactsList