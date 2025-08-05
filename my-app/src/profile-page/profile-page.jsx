import React from 'react'
import { useNavigate, Link } from 'react-router-dom'
import './profile-page.css'

function ProfilePage() {
  const username = localStorage.getItem('username') || 'Unknown User'
  const navigate = useNavigate()

  const handleSignOut = () => {
    localStorage.removeItem('username')
    navigate('/login')
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <h2 className="profile-title">Your Profile</h2>
        <div className="username-display">
          <strong>Username:</strong> {username}
        </div>

        <div className="nav-buttons">
          <Link to="/contacts-list">
            <button className="btn">Contacts</button>
          </Link>
          <Link to="/chat">
            <button className="btn">Chats</button>
          </Link>
          <Link to="/contacts">
            <button className="btn">Add Contact</button>
          </Link>
        </div>

        <div className="signout-container">
          <button className="btn btn-signout" onClick={handleSignOut}>
            Sign Out
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
