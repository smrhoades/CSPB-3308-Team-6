/*
This file defines the UserContext which will store the current user's data after
logging in.
To access the current user's data in other components, import useUser then do
    const {user, setUser, clearUser} = useUser();
to access user data and functions for setting/clearing user data.

The user data is sent by Flask after authenticating login (see backend/auth.py::login). 
The user object returned by useUser() will have the following form:
    {
      'user': {
        'username': username,
        'uuid': uuid
        }
    }

Basic idea:
- UserContext defines the data to be shared with other components.
- UserData is a "provider" component that creates storage space for the data.
- useUser is a custom hook that makes it easy for other components to use/access
  the Context.

Notes
- This component is just the "container" that holds the state (user, setUser) 
  and makes it available to other components. 
- Common React pattern: "provider" components that manage states but don't render
  any UI themselves, and "consumer" components that actually use the states.
*/

import { createContext, useContext, useState } from 'react'

const UserContext = createContext();

function UserData({ children }) {
    const [user, setUser] = useState({});

    const clearUser = () => {
        setUser({});
    }

    return (
        <UserContext.Provider value={{ user, setUser, clearUser }}> 
            {children}
        </UserContext.Provider>
    )
}

function useUser() {
    return useContext(UserContext);
}

export { UserData, useUser }