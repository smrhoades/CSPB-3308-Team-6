import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './login-page/login-page.jsx'
import RegisterPage from './register-page/register-page.jsx'
import ContactsList from './contacts-list/contacts-list.jsx'
import Contacts from './contacts/contacts.jsx'
import VisualMessagesList from './chat/chat.jsx'
import ProfilePage from './profile-page/profile-page.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"              element={<LoginPage/>} />
        <Route path="/login"         element={<LoginPage/>} />
        <Route path="/register"      element={<RegisterPage/>} />
        <Route path="/contacts-list" element={<ContactsList/>} />
        <Route path="/contacts"      element={<Contacts/>} />
        <Route path="/chat"          element={<VisualMessagesList/>} />
        <Route path="/profile-page"          element={<ProfilePage/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App