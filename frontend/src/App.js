import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import Friends from './components/Friends';
import Chat from './components/Chat';
import Profile from './components/Profile';
import Messages from './components/Messages';
import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      axios.get(`${API_URL}/users/`)
        .then(response => setUser(response.data))
        .catch(() => {
          setToken(null);
          localStorage.removeItem('token');
        });
    }
  }, [token, API_URL]);

  const handleLogout = async () => {
    try {
      await axios.post(`${API_URL}/users/logout`);
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar user={user} onLogout={handleLogout} />
      <Routes>
        <Route path="/" element={user ? <Navigate to="/friends" /> : <Login setUser={setUser} setToken={setToken} />} />
        <Route path="/register" element={user ? <Navigate to="/friends" /> : <Register setUser={setUser} setToken={setToken} />} />
        <Route path="/friends" element={user ? <Friends /> : <Navigate to="/" />} />
        <Route path="/chat/:conversationId" element={user ? <Chat user={user} /> : <Navigate to="/" />} />
        <Route path="/profile" element={user ? <Profile user={user} setUser={setUser} /> : <Navigate to="/" />} />
        <Route path="/messages" element={user ? <Messages user={user} /> : <Navigate to="/" />} />
      </Routes>
    </div>
  );
}

export default App;