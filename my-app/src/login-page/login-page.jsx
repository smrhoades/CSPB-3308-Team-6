import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './login-page.css'

// spatch = "http://127.0.0.1:5000/login"

function LoginPage() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleLogin = async () => {
        const requestBody = JSON.stringify({username, password})
        console.log(requestBody)                                                // for testing
        try {
            const response = await fetch('http://127.0.0.1:5000/auth/login',    // placeholder
            {
                method: 'POST',                                     
                headers: { 'Content-Type': 'application/json' },                // this is for Flask to understand that the request is a json
                body: requestBody                                               // converts the provided username, password into a json
            }
            );

            const data = await response.json();                                 // Flask's response will be saved in data
            console.log(data)                                                   // for testing

            if (data.status == 'success') {                                     
                navigate('/contacts-list')                                      // if successful, display the contacts-list page
                localStorage.setItem('username', username)
                navigate('/contacts-list')
            } else {            
                setError(`Login error with msg: ${data.message}`)               // Flask should tell us here that the credentials and invalid
                console.log(data)                                               // for testing - this shows us Flask's response
            }
        } catch (err) {
            setError('Server Error: no response from Flask')
        }

    };

    return (
        <div className="center-box">
            <h1>Welcome!</h1>
            <form onSubmit={(e) => {e.preventDefault(); handleLogin(); }}>
                <label>username</label>
                <br />
                <input id="username-input" className="login-input" value={username} onChange={(e) => setUsername(e.target.value)} />
                <br />
                <label>password</label>
                <br />
                <input id="password-input" className="login-input" value={password} onChange={(e) => setPassword(e.target.value)} type="password"/>
                <br />
                <button type ="submit" onClick={handleLogin}>login</button>
                <br />
                <Link to="/register">
                    <button>need to register?</button>
                </Link>
            </form>
        </div>
    )
}

export default LoginPage