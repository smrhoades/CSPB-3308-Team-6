import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './register-page.css'

function RegisterPage() {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleRegister = async () => {
    const requestBody = JSON.stringify({username, password})
    console.log(requestBody)                                    // for testing
    try {
        const response = await fetch('/api/endpoint',           // placeholder - should be our file structure or a proxy if we are testing
        {
            method: 'POST',                                     
            headers: { 'Content-Type': 'application/json' },    // this is for Flask to understand that the request is a json
            body: requestBody                                   // converts the provided username, password into a json
        }
        );

        const data = await response.json();                     // Flask's response will be saved in data
        console.log(data)                                       // for testing

        if (data.success) {                                     
            navigate('/login')                                  // if successful, return to login page
        } else {            
            setError(`Register error with msg: ${data.message}`)// Flask should tell us here that the credentials are invalid and why
        }
    } catch (err) {
        setError('Server Error: no response from Flask')
    }

    };

    return (
        <div className="center-box">
            <h1>Register Here</h1>
            <form onSubmit={(e) => {e.preventDefault(); handleRegister(); }}>
                <label>username</label>
                <br />
                <input id="username-input" className="login-input" value={username} onChange={(e) => setUsername(e.target.value)} />
                <br />
                <label>password</label>
                <br />
                <input id="password-input" className="login-input" value={password} onChange={(e) => setPassword(e.target.value)} type="password"/>
                <br />
                <button type ="submit" onClick={handleRegister}>register</button>
                <br />
            </form>
        </div>
    )
}

export default RegisterPage