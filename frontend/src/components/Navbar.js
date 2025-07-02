import { Link } from "react-router-dom";
import { useState } from "react";

function Navbar({ user, onLogout }) {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleDropdown = () => {
    setMenuOpen((prev) => !prev);
  };

  return (
    <nav className="bg-blue-500 p-4 text-white">
      <div className="max-w-4xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <img
            src="/images/homie_logo.jpg" 
            alt="Logo"
            className="w-12 h-12 object-contain"
          />
          <h1 className="text-xl font-bold">Homie Chat</h1>
        </div>

        <div className="flex items-center space-x-6">
          {user ? (
            <>
              <div className="flex space-x-4">
                <Link to="/messages" className="hover:underline">
                  Messages
                </Link>
                <Link to="/friends" className="hover:underline">
                  Friends
                </Link>
              </div>

              <div className="relative ml-auto">
                <div
                  className="flex items-center space-x-2 cursor-pointer"
                  onClick={toggleDropdown}
                >
                  <img
                    src={user.avatar || "/images/avatar_df.jpg"}
                    alt="Avatar"
                    className="w-10 h-10 rounded-full object-cover"
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = "/images/avatar_df.jpg";
                    }}
                  />
                  <span className="hover:underline">{user.name || "User"}</span>
                </div>

                {menuOpen && (
                  <div className="absolute right-0 mt-2 w-40 bg-white text-black rounded shadow-lg z-10">
                    <Link
                      to="/profile"
                      className="block px-4 py-2 hover:bg-gray-100"
                      onClick={() => setMenuOpen(false)}
                    >
                      Profile
                    </Link>
                    <button
                      onClick={() => {
                        setMenuOpen(false);
                        onLogout();
                      }}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <Link to="/" className="hover:underline">
                Login
              </Link>
              <Link to="/register" className="hover:underline">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
