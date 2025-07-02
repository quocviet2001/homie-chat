from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from .routes.conversation import router as conversation_router
from .websocket.chat import router as websocket_router

app = FastAPI(
    title="Homie Chat Service",
    description="Chat Service for Homie Chat application",
    version="1.0.0",
    redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversation_router)
app.include_router(websocket_router, prefix="/ws")

@app.get("/")
async def root():
    return {"message": "Homie Chat Service is running"}
