# Import FastAPI để tạo ứng dụng API
from fastapi import FastAPI
# Import MongoClient từ pymongo để kết nối với MongoDB
from pymongo import MongoClient

# Khởi tạo ứng dụng FastAPI với metadata
app = FastAPI(
    title="Homie Chat Service",
    description="Chat Service for Homie real-time chat application",
    version="1.0.0"
)

# Kết nối với MongoDB server chạy trên localhost, port mặc định 27017
client = MongoClient("mongodb://localhost:27017")
# Chọn database 'homie_chat' (sẽ tự động tạo nếu chưa tồn tại)
db = client["homie_chat"]
# Chọn collection 'conversations' để lưu thông tin hộp thoại
conversations_collection = db["conversations"]
# Chọn collection 'messages' để lưu tin nhắn
messages_collection = db["messages"]

# Route GET cơ bản để kiểm tra trạng thái Chat Service
@app.get("/")
async def root():
    # Trả về JSON để xác nhận service đang chạy
    return {"message": "Homie Chat Service is running"}

# Route GET để kiểm tra kết nối với MongoDB
@app.get("/test-mongo")
async def test_mongo():
    test_doc = {"test_key": "MongoDB connection test", "created_at": "2025-05-28"}
    result = conversations_collection.insert_one(test_doc)
    
    # Gán _id vừa được tạo vào test_doc, convert sang chuỗi
    test_doc["_id"] = str(result.inserted_id)
    
    return {
        "message": "MongoDB connection successful",
        "inserted_doc": test_doc
    }


# Xử lý ngắt kết nối MongoDB khi ứng dụng dừng (optional cleanup)
@app.on_event("shutdown")
def shutdown_event():
    # Đóng kết nối MongoDB để tránh rò rỉ tài nguyên
    client.close()