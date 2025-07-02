from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from ..middlewares.auth import get_current_user_ws
import websockets
import os
import asyncio
import httpx

router = APIRouter()

CHAT_SERVICE_WS_URL = os.getenv("CHAT_SERVICE_URL").replace("http", "ws")
CHAT_SERVICE_API_URL = os.getenv("CHAT_SERVICE_URL")

@router.websocket("/chat/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str, token: str):
    user = await get_current_user_ws(token)
    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return

    # Kiểm tra quyền truy cập conversation
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{CHAT_SERVICE_API_URL}/conversations/{conversation_id}/messages",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                await websocket.close(code=1008, reason="Unauthorized or invalid conversation")
                return
        except httpx.HTTPError:
            await websocket.close(code=1008, reason="Failed to verify conversation")
            return

    await websocket.accept()

    try:
        async with websockets.connect(
            f"{CHAT_SERVICE_WS_URL}/ws/chat/{conversation_id}?token={token}"
        ) as service_ws:
            client_to_service = asyncio.create_task(forward_client_to_service(websocket, service_ws))
            service_to_client = asyncio.create_task(forward_service_to_client(websocket, service_ws))

            await asyncio.wait([client_to_service, service_to_client], return_when=asyncio.FIRST_COMPLETED)

    except websockets.exceptions.ConnectionClosed:
        await websocket.close(code=1000, reason="Chat Service disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close(code=1008, reason="Internal server error")

async def forward_client_to_service(websocket: WebSocket, service_ws: websockets.WebSocketClientProtocol):
    """Chuyển tin nhắn từ client đến Chat Service"""
    try:
        while True:
            data = await websocket.receive_text()
            await service_ws.send(data)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})

async def forward_service_to_client(websocket: WebSocket, service_ws: websockets.WebSocketClientProtocol):
    """Chuyển tin nhắn từ Chat Service đến client"""
    try:
        while True:
            response = await service_ws.recv()
            await websocket.send_text(response)
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})