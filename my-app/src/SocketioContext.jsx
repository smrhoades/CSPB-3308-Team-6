/*
This file defines the SocketIO Context that manages the SocketIO connection.

Notes
- Currently this Context wraps all routes so even unauthenticated users will 
  have a SocketIO connection, which is definitely not what we would want long-
  term. But I didn't want to have to deal with wrapping individual routes when
  setting this up initially.

- A SocketIO instance is created when any wrapped component is mounted.
  Because useRef is used, the instance is not re-created on re-renders (but it
  is re-created on re-mounts.) This is good because the component will re-render
  each time a message is sent.  
  
- Event listeners are registered when the component mounts. 

- joinRoom and sendMessage are defined with useCallback because useCallback 
  memoizes the functions. In this way, the send function doesn't need to be
  recalculated each time a user sends a message. 

- The elegant part is how incoming messages are routed to the appropriate chat
  component. The Socket.IO documentation "strongly recommends" against registering
  event listeners in child components, so handling should occur here. But how 
  to pass the data to the correct component?
  The solution is to create a mapping from room_ids to handler functions, such that
  each room can define their own handler and subscribe/register it with the Context-
  defined mapping. This is what the subscribeToRoom function does. The actual
  event listener (socketRef.current.on('message',...)) is registered here in the
  Context, but it then calls the room-specific handler, passing the message data
  as argument. Thus, the appropriate Chat component can receive incoming mesasges. 

- Socket.IO documentation: https://socket.io/how-to/use-with-react
*/

import { createContext, useContext, useEffect, useRef, useState, useCallback } from 'react';
import { io } from 'socket.io-client';

const SocketioContext = createContext();

export function SocketioConnection({ children } ) {
    // state and refs
    const socketRef = useRef(null);
    const [connState, setConnState] = useState('disconnected');
    const [error, setError] = useState(null);
    const messageHandlers = useRef(new Map()); // Map of roomId -> handler function

    useEffect(() => {
        // establish connection with '/chat' namespace
        socketRef.current = io('http://127.0.0.1:5000/chat', {
          withCredentials: true
        });
        
        // register event listeners
        socketRef.current.on('connect', () => {
            setConnState('connected');
        });

        socketRef.current.on('disconnect', () => {
            setConnState('disconnected');
        });

        socketRef.current.on('message', (msg) => {
            // TO DO: Flask should send room_id with data
            const { room_id } = msg;
            const handler = messageHandlers.current.get(room_id);
            if (handler) {
                handler(msg);
            }
        });

        socketRef.current.on('room_joined', (data) => {
            console.log("room_joined event logged with data:", data);
        });

        return () => {
            socketRef.current.disconnect();
        };

    }, []);

    // functions that use useCallback
    const joinRoom = useCallback((roomId) => {
        if (socketRef.current && socketRef.current.connected) {
            socketRef.current.emit('join', {'room': roomId});
        }
        else {
            setError("Couldn't join room: socketio not connected", error);
        }
    }, []);

    const sendMessage = useCallback((to, message) => {
        if (socketRef.current && socketRef.current.connected) {
            console.log("Message to send:", message);
            console.log("To send to:", to);
            socketRef.current.send([{'recipient_user_name': to, 'message': message}]);
        }
        else {
            setError("Couldn't send message: no connection", error);
        }
    }, []);

    const subscribeToRoom = useCallback((roomId, handler) => {
        messageHandlers.current.set(roomId, handler);

        // Return cleanup function
        return () => {
            messageHandlers.current.delete(roomId);
        };
    }, []);

    return (
        <SocketioContext.Provider value={{
            connState, joinRoom, sendMessage, subscribeToRoom, error
        }}>
            {children}
        </SocketioContext.Provider>
    );
}

export const useSocket = () => {
    return useContext(SocketioContext);
};