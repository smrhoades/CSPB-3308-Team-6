import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './login-page/login-page.jsx'
import RegisterPage from './register-page/register-page.jsx'
import ContactsList from './contacts-list/contacts-list.jsx'
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
                <Route path="/contacts-list" element={<ContactsList/>} />
                <Route path="/contacts"      element={<Contacts/>} />
                <Route path="/chat/:room_id" element={<ChatContainer/>} />
            </Routes>
            </BrowserRouter>
        </SocketioConnection>
    </UserData>
  )
}

export default App