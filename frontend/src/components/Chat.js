import { useState, useEffect } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

function Chat({ user }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [error, setError] = useState(null);
  const [ws, setWs] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const { conversationId } = useParams();
  const navigate = useNavigate();
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  const WS_URL =  process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

  useEffect(() => {
    fetchMessages();
    connectWebSocket();

    return () => {
      if (ws) ws.close();
    };
  }, [conversationId]);

  const fetchMessages = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/chat/conversations/${conversationId}/messages`
      );
      setMessages(response.data);
    } catch (error) {
      setError(error.response?.data?.error || "Failed to fetch messages");
    }
  };

  const connectWebSocket = () => {
    const token = localStorage.getItem("token");
    const websocket = new WebSocket(
      `${WS_URL}/ws/chat/${conversationId}?token=${token}`
    );
    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.sender_id !== user.id.toString()) {
        setMessages((prev) => [...prev, message]);
      }
    };
    websocket.onerror = () => {
      setError("WebSocket connection failed");
    };
    setWs(websocket);
  };

  const sendMessage = () => {
    if (newMessage.trim() && ws && ws.readyState === WebSocket.OPEN) {
      const message = {
        content: newMessage,
        sender_id: user.id.toString(),
        timestamp: new Date().toISOString(),
      };
      ws.send(JSON.stringify(message)); 
      setMessages((prev) => [...prev, message]);
      setNewMessage("");
    }
  };

  const searchMessages = async () => {
    try {
      const params = { conversation_id: conversationId };
      if (searchQuery) params.query = searchQuery;
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;
      const response = await axios.get(
        `${API_URL}/chat/conversations/messages/search`,
        { params }
      );
      setMessages(response.data);
      setError(null);
    } catch (error) {
      setError(error.response?.data?.error || "Failed to search messages");
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-8 p-4">
      <h2 className="text-2xl font-bold mb-4">Chat</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="mb-4 flex flex-col md:flex-row gap-2">
        <input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search messages"
          className="p-2 border rounded flex-grow"
        />
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="p-2 border rounded"
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="p-2 border rounded"
        />
        <button
          onClick={searchMessages}
          className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Search
        </button>
        <button
          onClick={fetchMessages}
          className="bg-gray-500 text-white p-2 rounded hover:bg-gray-600"
        >
          Clear
        </button>
      </div>
      <div className="bg-white rounded shadow p-4 mb-4 h-96 overflow-y-auto">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-2 flex ${
              message.sender_id === user.id.toString()
                ? "justify-end"
                : "justify-start"
            }`}
          >
            <div
              className={`p-2 rounded ${
                message.sender_id === user.id.toString()
                  ? "bg-blue-100"
                  : "bg-gray-100"
              }`}
            >
              <span className="font-bold">
                {message.sender_id === user.id.toString() ? "You" : "Friend"}:
              </span>
              {message.content}{" "}
              <small className="text-gray-500">{message.timestamp}</small>
            </div>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyUp={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type a message"
          className="p-2 border rounded flex-grow"
        />
        <button
          onClick={sendMessage}
          className="ml-2 bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Send
        </button>
      </div>
      <button
        onClick={() => navigate("/friends")}
        className="mt-4 bg-gray-500 text-white p-2 rounded hover:bg-gray-600"
      >
        Back to Friends
      </button>
    </div>
  );
}

export default Chat;
