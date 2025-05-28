# Import FastAPI để tạo ứng dụng API
from fastapi import FastAPI

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Homie Chat API Gateway",
    description="API Gateway for Homie Chat application",
    version="1.0.0"
)

# Route cơ bản để kiểm tra API Gateway
@app.get("/")
async def root():
    # Trả về JSON để xác nhận API Gateway hoạt động
    return {"message": "Homie Chat API Gateway is running"}
