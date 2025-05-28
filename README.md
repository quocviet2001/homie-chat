homie-chat/
├── api-gateway/                  # FastAPI: API Gateway
│   ├── app/
│   │   ├── main.py               # File chính khởi chạy API Gateway
│   │   ├── routes/              # Các endpoint REST
│   │   ├── websocket/           # Xử lý WebSocket
│   │   └── middlewares/         # Middleware xác thực JWT
│   └── requirements.txt         # Các thư viện Python

├── user-service/                # Laravel: User Service
│   ├── app/
│   │   ├── Models/              # Model: User, Friend, FriendRequest
│   │   └── Http/
│   │       ├── Controllers/     # Controller cho API
│   │       └── Middleware/      # Middleware xác thực
│   ├── routes/
│   │   └── api.php              # Định nghĩa các route API
│   ├── database/
│   │   ├── migrations/          # Migration cho PostgreSQL
│   │   └── seeders/             # Dữ liệu mẫu
│   └── composer.json            # Các thư viện PHP

├── chat-service/                # FastAPI: Chat Service
│   ├── app/
│   │   ├── main.py              # File chính khởi chạy Chat Service
│   │   ├── routes/              # Các endpoint REST
│   │   ├── websocket/           # Xử lý WebSocket cho chat
│   │   └── models/              # Định nghĩa schema MongoDB
│   └── requirements.txt         # Các thư viện Python

├── frontend/                    # Vue.js: Frontend
│   ├── src/
│   │   ├── components/          # Các component Vue (ChatBox, FriendList, v.v.)
│   │   ├── views/               # Các trang (Login, Chat, Friends)
│   │   ├── store/               # Pinia/Vuex để quản lý trạng thái
│   │   ├── router/              # Vue Router
│   │   └── assets/              # CSS, hình ảnh
│   ├── public/                  # Tệp tĩnh
│   └── package.json             # Các thư viện JS

├── docs/                        # Tài liệu (API specs, hướng dẫn)
└── README.md                    # Mô tả dự án
