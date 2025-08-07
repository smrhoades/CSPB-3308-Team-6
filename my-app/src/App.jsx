import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './login-page/login-page.jsx'
import RegisterPage from './register-page/register-page.jsx'
import NavBar from './navbar/navbar.jsx'
import Contacts from './contacts/contacts.jsx'
import ChatContainer from './chat/chat.jsx'
import { UserData } from './UserContext.jsx'
import { SocketioConnection } from './SocketioContext.jsx'


function App() {
  // Wrap all routes in UserData context: before logging in, user object will be {}
  // After logging in, user data will be able to accessed (see UserContext.jsx)
  return (
    <UserData>
        <SocketioConnection>
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
            </Routes>
            </BrowserRouter>
        </SocketioConnection>
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