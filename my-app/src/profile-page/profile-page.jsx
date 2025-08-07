import { useUser } from '../UserContext.jsx'
import './profile-page.css'

function ProfilePage() {
  const { user } = useUser();
  const username = user.username;
  return (
    <div className="profile-container">
      <div className="profile-card">
        <h2 className="profile-title">Your Profile</h2>
        <div className="username-display">
          <strong>Username:</strong> {username}
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
