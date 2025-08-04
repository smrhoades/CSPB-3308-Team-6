import './contacts.css'
import { useEffect, useState } from 'react'
import { useUser } from '../UserContext.jsx'

/*
Pattern
    1. Component loads (ContactsList renders)
    2. useEffect runs and calls getContacts
    3. getContacts fetches data from Flask
    4. Store the fetched data in component state using useState
    5. Component re-renders with the new data

TO DO:
- User's username is not displayed in the welcome message when page is refreshed.

*/

// const contactsArray = ['John','Paul','George','Ringo'];

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
    // hooks are called at top level of component so that the states they modify
    // persist across renders
    const [contacts, setContacts] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        getContacts();
    }, []);

    const getContacts = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/contacts', { 
                method: 'GET', 
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'  // send cookies with the request so Flask knows User is logged-in
            });
            const data = await response.json();
            // extract contact names from received data
            console.log(data.contacts_data);
            const contactNames = data.contacts_data.map(contact => contact.contact_name);
            console.log(contactNames);
            setContacts(contactNames);
        }
        catch (err) {
            setError('Failed to retrieve contacts');
        }
    }

    const {user, setUser, clearUser} =  useUser();

    return (
        <div className="center-box" id="outer-box">
            <h1>Welcome {user.username}!</h1>
            <h1>Contacts</h1>
            <VisualContactsList contacts={contacts}/>
        </div>
    )
}

export default ContactsList