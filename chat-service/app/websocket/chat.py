from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from bson import ObjectId
from datetime import datetime
from jose import JWTError, jwt
from ..database import messages_collection, conversations_collection
import os

JWT_SECRET = os.getenv("JWT_SECRET")

router = APIRouter()

active_connections = {}

@router.websocket("/chat/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str, token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    conversation = conversations_collection.find_one({
        "_id": ObjectId(conversation_id),
        "user_ids": user_id
    })
    if not conversation:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    if conversation_id in active_connections:
        active_connections[conversation_id] = [
            conn for conn in active_connections[conversation_id]
            if conn["user_id"] != user_id
        ]
    else:
        active_connections[conversation_id] = []

    active_connections[conversation_id].append({
        "user_id": user_id,
        "websocket": websocket
    })

    try:
        while True:
            data = await websocket.receive_json()
            message = {
                "conversation_id": ObjectId(conversation_id),
                "sender_id": user_id,
                "content": data["content"],
                "timestamp": datetime.utcnow()
            }
            messages_collection.insert_one(message)

            for connection in active_connections.get(conversation_id, []):
                if connection["user_id"] != user_id: 
                    await connection["websocket"].send_json({
                        "sender_id": user_id,
                        "content": data["content"],
                        "timestamp": message["timestamp"].isoformat()
                    })

    except WebSocketDisconnect:
        active_connections[conversation_id] = [
            conn for conn in active_connections[conversation_id]
            if conn["websocket"] != websocket
        ]
        if not active_connections[conversation_id]:
            del active_connections[conversation_id]
    except Exception as e:
        await websocket.close(code=1008)