import './addContact.css'
import { useState, useEffect } from 'react'
import { VisualContactsList } from '../contacts.jsx'

export default function AddContact() {
    const [ searchTerm, setSearchTerm ] = useState('');
    const [ searchData, setSearchData ] = useState([]);
    const [ feedback, setFeedback ] = useState('');
    const [ error, setError ] = useState('');

    useEffect(() => {
        if (feedback !== '') alert(feedback);
        setFeedback('');
    }, [feedback]);

    const searchUser = async (searchTerm) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/users/search?username=${searchTerm}`,
                {
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include'
                }
            );
            const data = await response.json();
            if (data.message == "success") {
                setSearchData(data.users);
            }
            else {
                setSearchData(data.users);
                setFeedback(data.message);
            }
        }
        catch (e) {
            setError("Couldn't fetch search results", e);
            console.log("got error", error);
        }
    }

    const addContact = async (contact) => {
        if (!confirm(`Add ${contact.user_name} to contacts?`)) return;

        try {
            const response = await fetch(`http://127.0.0.1:5000/contacts`,
                {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({'username': contact.user_name}),
                    credentials: 'include'
                }
            );
            const data = await response.json();
            setFeedback(data.message);
            console.log('got message', data.message)
        }
        catch (e) {
            setError("Couldn't add contact", e);
            console.log(error);
        }
    };

    return (
        <div className="page-container">
            <div className="searchBar">
                <input id="searchField"
                    value={searchTerm}
                    onChange={(e) => { setSearchTerm(e.target.value) }}
                    onKeyDown={(e) => e.key === 'Enter' && searchUser(searchTerm)}
                />
                <button type="button" id="searchButton" onClick={(e) => searchUser(searchTerm)}>search</button>
            </div>
            <div>
                <VisualContactsList contacts={searchData}
                                    clickHandler={addContact}
                                    idProperty="uuid"
                                    displayProperty="user_name"
                />
            </div>
        </div>
    )
}