import './navbar.css'
import { useNavigate, Link } from 'react-router-dom'
import { useState } from 'react'
import { useUser } from '../UserContext.jsx'

export default function NavBar() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const { clearUser } = useUser();
    const navigate = useNavigate();

    const handleLogout = async () => {
        setIsLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/auth/logout', { credentials: 'include' });
            console.log(response)
            if (response.status == 200) {
                setIsLoading(false);
                clearUser();
                navigate('/login');
            } else {
                setIsLoading(false);
                alert('Logout failed');
            }
        } catch (e) {
            setIsLoading(false);
            setError(e);
            alert(`Logout failed: ${error}`);
        }
    };

    return (
        <nav className="navbar">
            <Link to='/contacts'>
                <button className="nav-item">My Contacts</button>
            </Link>
            <Link to='/contacts/add'>
            <button className="nav-item">Add Contact</button>
            </Link>
            <Link to='/profile'>
                <button className="nav-item">Profile</button>
            </Link>
            <button className="nav-item" onClick={handleLogout} disabled={isLoading}>
                {isLoading ? "Logging out..." : "Logout"}
            </button>
        </nav>
    )
}

