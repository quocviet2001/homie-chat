from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from .routes.user import router as user_router
from .routes.chat import router as chat_router
from .websocket.chat import router as websocket_router

app = FastAPI(
    title="Homie Chat API Gateway",
    description="API Gateway for Homie Chat application",
    version="1.0.0"
)

# Thêm middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(user_router)
app.include_router(chat_router)
app.include_router(websocket_router, prefix="/ws")

@app.get("/")
async def root():
    return {"message": "Homie Chat API Gateway is running"}
