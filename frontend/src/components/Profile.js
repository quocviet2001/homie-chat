import { useState, useEffect } from 'react';
import axios from 'axios';

function Profile({ user, setUser }) {
  const [formData, setFormData] = useState({
    name: user?.name || '',
    phone: user?.phone || '',
    avatar: user?.avatar || ''
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name,
        phone: user.phone,
        avatar: user.avatar
      });
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put(`${API_URL}/users/`, formData);
      setUser(response.data.user);
      setSuccess('Profile updated successfully');
      setError(null);
      setIsEditing(false);
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to update profile');
      setSuccess(null);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-4 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Profile</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {success && <p className="text-green-500 mb-4">{success}</p>}
      {!isEditing ? (
        <div>
          <div className="mb-4">
            <label className="block mb-1 font-semibold">Name</label>
            <p>{user?.name}</p>
          </div>
          <div className="mb-4">
            <label className="block mb-1 font-semibold">Email</label>
            <p>{user?.email}</p>
          </div>
          <div className="mb-4">
            <label className="block mb-1 font-semibold">Phone</label>
            <p>{user?.phone || 'Not set'}</p>
          </div>
          <div className="mb-4">
            <label className="block mb-1 font-semibold">Avatar</label>
            {user?.avatar ? (
              <img src={user.avatar} alt="Avatar" className="w-24 h-24 rounded" />
            ) : (
              <p>Not set</p>
            )}
          </div>
          <button
            onClick={() => setIsEditing(true)}
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            Edit Profile
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-1">Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Phone</label>
            <input
              type="text"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="mb-4">
            <label className="block mb-1">Avatar URL</label>
            <input
              type="text"
              name="avatar"
              value={formData.avatar}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="flex space-x-2">
            <button
              type="submit"
              className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Save
            </button>
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className="w-full bg-gray-500 text-white p-2 rounded hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default Profile;