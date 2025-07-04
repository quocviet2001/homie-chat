import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function Messages({ user }) { 
  const [conversations, setConversations] = useState([]);
  const [friends, setFriends] = useState([]); 
  const [error, setError] = useState(null);
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchFriends(); 
    fetchConversations();
  }, []);

  const fetchFriends = async () => {
    try {
      const response = await axios.get(`${API_URL}/users/friends`);
      setFriends(response.data);
    } catch (error) {
      setError(error.response?.data?.detail || error.response?.data?.error || 'Failed to fetch friends');
    }
  };

  const fetchConversations = async () => {
    try {
      const response = await axios.get(`${API_URL}/chat/conversations`);
      setConversations(response.data);
      setError(null);
    } catch (error) {
      setError(error.response?.data?.detail || error.response?.data?.error || 'Failed to fetch conversations');
    }
  };

  const getFriendName = (userIds) => {
    const friendId = userIds.find(id => id !== user.id.toString());
    const friend = friends.find(f => f.id.toString() === friendId);
    return friend ? friend.name : 'Unknown User';
  };

  return (
    <div className="max-w-4xl mx-auto mt-8 p-4">
      <h2 className="text-2xl font-bold mb-4">Messages</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {conversations.length === 0 && !error && (
        <p className="text-gray-500">No conversations yet.</p>
      )}
      <ul className="bg-white rounded shadow">
        {conversations.map(conversation => (
          <li key={conversation._id} className="border-b border-gray-300 last:border-b-0 p-4 hover:bg-gray-50 transition">
            <Link
              to={`/chat/${conversation._id}`}
              className="text-blue-500 hover:underline"
            >
            {getFriendName(conversation.user_ids)} 
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Messages;