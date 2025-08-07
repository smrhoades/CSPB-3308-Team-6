import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './login-page/login-page.jsx'
import RegisterPage from './register-page/register-page.jsx'
import NavBar from './navbar/navbar.jsx'
import Contacts from './contacts/contacts.jsx'
import ChatContainer from './chat/chat.jsx'
import ProfilePage from './profile-page/profile-page.jsx'
import { UserData } from './UserContext.jsx'
import { SocketioConnection } from './SocketioContext.jsx'


function App() {
  // Wrap all routes in UserData context: before logging in, user object will be {}
  // After logging in, user data will be able to accessed (see UserContext.jsx)
  return (
    <UserData>
            <BrowserRouter>
            <Routes>
                <Route path="/"              element={<LoginPage/>} />
                <Route path="/login"         element={<LoginPage/>} />
                <Route path="/register"      element={<RegisterPage/>} />
                <Route path="/contacts"      element={<AuthenticatedRoute>
                                                        <Contacts/>
                                                      </AuthenticatedRoute>} />
                <Route path="/chat/:roomId" element={<AuthenticatedRoute>
                                                        <ChatContainer/>
                                                     </AuthenticatedRoute>} />
                <Route path="/profile" element={<AuthenticatedRoute>
                                                    <ProfilePage/>
                                                </AuthenticatedRoute>} />
            </Routes>
            </BrowserRouter>
    </UserData>
  )
}

function AuthenticatedRoute({ children }) {
    return (
        <div>
            <SocketioConnection>
                <AuthenticatedLayout>
                    {children}
                </AuthenticatedLayout>
            </SocketioConnection>
        </div>
    )
}

function AuthenticatedLayout({ children }) {
    return (
        <div>
            <NavBar />
                {children}
        </div>
    );
}

export default App