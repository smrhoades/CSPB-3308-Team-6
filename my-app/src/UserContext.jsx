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

import { createContext, useContext, useState, useEffect } from 'react'

const UserContext = createContext();

function UserData({ children }) {
    const [user, setUser] = useState({});
    const [isLoading, setIsLoading] = useState(true); // track loading state

    // Check for existing session on app startup
    useEffect(() => {
        const checkCurrentUser = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/auth/current-user', {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include' // include session cookers
                });

                if (response.ok) {
                    const userData = await response.json();
                    setUser(userData); // Restore user data
                } else {
                    // No valid session, user stays empty
                    console.log('No active session found');
                }
            } catch (err) {
                console.log('Failed to check user session:', err);
                // User stays empty on error
            } finally {
                setIsLoading(false); // Done checking
            }
        }

        checkCurrentUser();
    }, []); // Run once on mount

    const clearUser = () => {
        console.log('User', user.username, 'logged out');
        setUser({});
    }

    return (
        <UserContext.Provider value={{ user, setUser, clearUser, isLoading }}> 
            {children}
        </UserContext.Provider>
    )
}

function useUser() {
    return useContext(UserContext);
}

export { UserData, useUser }