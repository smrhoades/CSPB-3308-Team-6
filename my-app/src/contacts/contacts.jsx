import { Link, useNavigate } from 'react-router-dom'
import './contacts.css'

const userID = 1
const contactsArray = ['Paul','George','Ringo'];
const contactIDsArray = [2,3,4];


function VisualContactsList({ contacts }) {
    const navigate = useNavigate()
    function handleClick(event) {
        const clickedUserID = Number(event.currentTarget.dataset.userid)
        const roomID = Math.min(userID+clickedUserID, clickedUserID+userID)
        const rootDirectory = 'http://127.0.0.1:5000'
        const roomIDendpoint = `/chat/${roomID}`
        console.log(`clicked div with id: ${clickedUserID}`)
        navigate(roomIDendpoint)
    }


    return (
            <>
                {
                    contacts.map((contactName, index) => (
                        <div 
                            className="contact-card" 
                            key={index}
                            id={`contactid-${contactIDsArray[index]}`}
                            data-userid={contactIDsArray[index]}
                            onClick={handleClick}
                        >{contactName}</div>
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