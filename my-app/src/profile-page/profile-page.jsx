import React from 'react'
import { useNavigate } from 'react-router-dom'
import './profile-page.css'

function ProfilePage() {
  // Read the username set at login
  const username = localStorage.getItem('username') || 'Unknown User'
  const navigate = useNavigate()

  const handleSignOut = () => {
    // Clear stored username and redirect to login
    localStorage.removeItem('username')
    navigate('/login')
  }

  return (
    <div className="profile-container">
      <div className="username-display">
        Username: {username}
      </div>
      <div className="signout-container">
        <button onClick={handleSignOut}>Sign Out</button>
      </div>
    </div>
  )
}

export default ProfilePage
