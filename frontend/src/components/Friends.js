import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { debounce } from "lodash";

function Friends() {
  const [friends, setFriends] = useState([]);
  const [friendRequests, setFriendRequests] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchFriends();
    fetchFriendRequests();
  }, []);

  const fetchFriends = async () => {
    try {
      const response = await axios.get(`${API_URL}/users/friends`);
      setFriends(response.data);
    } catch (error) {
      setError(error.response?.data?.error || "Failed to fetch friends");
    }
  };

  const fetchFriendRequests = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/users/friend-requests`
      );
      setFriendRequests(response.data);
    } catch (error) {
      setError(
        error.response?.data?.error || "Failed to fetch friend requests"
      );
    }
  };

  const debouncedSearch = useCallback(
    debounce(async (query) => {
      if (!query) {
        setSearchResults([]);
        return;
      }
      try {
        const response = await axios.get(
          `${API_URL}/users/friends/search`,
          {
            params: { query },
          }
        );
        setSearchResults(response.data);
        setError(null);
      } catch (error) {
        setError(error.response?.data?.error || "Failed to search friends");
      }
    }, 500),
    []
  );

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    debouncedSearch(query);
  };

  const sendFriendRequest = async (receiverId) => {
    try {
      await axios.post(`${API_URL}/users/friend-requests`, {
        receiver_id: receiverId,
      });
      setSuccess("Friend request sent successfully");
      setSearchResults((prev) =>
        prev.map((user) =>
          user.id === receiverId ? { ...user, requestSent: true } : user
        )
      );
      setTimeout(() => setSuccess(null), 3000);
    } catch (error) {
      setError(error.response?.data?.error || "Failed to send friend request");
    }
  };

  const respondFriendRequest = async (requestId, status) => {
    try {
      await axios.put(`${API_URL}/users/friend-requests`, {
        request_id: requestId,
        status,
      });
      await fetchFriends();
      await fetchFriendRequests();
      // Reset requestSent trong searchResults nếu từ chối
      if (status === "rejected") {
        setSearchResults((prev) =>
          prev.map((user) =>
            user.id === requestId ? { ...user, requestSent: false } : user
          )
        );
      }
      setSuccess(`Friend request ${status}`);
      setTimeout(() => setSuccess(null), 3000);
    } catch (error) {
      setError(
        error.response?.data?.error || `Failed to ${status} friend request`
      );
    }
  };

  // Kiểm tra hoặc tạo hộp thoại trước khi chat
  const startChat = async (friendId) => {
    try {
      // Lấy danh sách hộp thoại
      const convResponse = await axios.get(
        `${API_URL}/chat/conversations`
      );
      const conversations = convResponse.data;

      // Tìm hộp thoại hiện có
      const existingConversation = conversations.find(
        (conv) =>
          conv.user_ids.includes(friendId.toString()) &&
          conv.user_ids.length === 2
      );

      if (existingConversation) {
        // Nếu hộp thoại tồn tại, điều hướng trực tiếp
        navigate(`/chat/${existingConversation._id}`);
      } else {
        // Nếu không, tạo hộp thoại mới
        const response = await axios.post(
          `${API_URL}/chat/conversations`,
          { friend_id: friendId.toString() }
        );
        navigate(`/chat/${response.data._id}`);
      }
    } catch (error) {
      setError(
        error.response?.data?.detail ||
          error.response?.data?.error ||
          "Failed to start chat"
      );
      setTimeout(() => setError(null), 3000);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-8 p-4">
      <h2 className="text-2xl font-bold mb-4">Friends</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {success && <p className="text-green-500 mb-4">{success}</p>}
      <div className="mb-4">
        <input
          value={searchQuery}
          onChange={handleSearch}
          placeholder="Search friends"
          className="w-full p-2 border rounded"
        />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 className="text-lg font-semibold mb-2">Your Friends</h3>
          <ul className="bg-white rounded shadow p-4">
            {friends.map((friend) => (
              <li
                key={friend.id}
                className="mb-2 flex justify-between items-center"
              >
                <span>{friend.name}</span>
                <button
                  onClick={() => startChat(friend.id)}
                  className="text-blue-500 hover:underline"
                >
                  Chat
                </button>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-2">Friend Requests</h3>
          <ul className="bg-white rounded shadow p-4">
            {friendRequests.map((request) => (
              <li
                key={request.id}
                className="mb-2 flex justify-between items-center"
              >
                <span>{request.sender.name || "Unknown User"}</span>
                <div>
                  <button
                    onClick={() => respondFriendRequest(request.id, "accepted")}
                    className="text-green-500 mr-2 hover:underline"
                  >
                    Accept
                  </button>
                  <button
                    onClick={() => respondFriendRequest(request.id, "rejected")}
                    className="text-red-500 hover:underline"
                  >
                    Reject
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {searchResults.length > 0 && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">Search Results</h3>
          <ul className="bg-white rounded shadow p-4">
            {searchResults.map((user) => (
              <li
                key={user.id}
                className="mb-2 flex justify-between items-center"
              >
                <span>{user.name}</span>
                <button
                  onClick={() => sendFriendRequest(user.id)}
                  disabled={user.requestSent}
                  className={`text-blue-500 hover:underline ${
                    user.requestSent ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                >
                  {user.requestSent ? "Request Sent" : "Add Friend"}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Friends;
