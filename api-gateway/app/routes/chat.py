from fastapi import APIRouter, Depends, HTTPException
from app.middlewares.auth import get_current_user
import httpx
import os
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

CHAT_SERVICE_URL = os.getenv("CHAT_SERVICE_URL")

# Định tuyến yêu cầu đến Chat Service
async def forward_request(method: str, path: str, **kwargs):
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(
                    f"{CHAT_SERVICE_URL}/{path}",
                    params=kwargs.get("params", {}),
                    headers=kwargs.get("headers", {})
                )
            elif method == "POST":
                response = await client.post(
                    f"{CHAT_SERVICE_URL}/{path}",
                    json=kwargs.get("data", {}),
                    headers=kwargs.get("headers", {})
                )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.text
            )

# Định nghĩa schema cho tạo hộp thoại
class ConversationCreate(BaseModel):
    friend_id: str
# Tạo hộp thoại mới
@router.post("/conversations")
async def create_conversation(conversation: ConversationCreate, current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "POST", "conversations",
        headers={"Authorization": f"Bearer {current_user['token']}"},
        data=conversation.dict()
    )

# Lấy danh sách hộp thoại
@router.get("/conversations")
async def get_conversations(current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "GET", "conversations",
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

# Lấy lịch sử tin nhắn
@router.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str, current_user: dict = Depends(get_current_user)):
    return await forward_request(
        "GET", f"conversations/{conversation_id}/messages",
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )

# Tìm kiếm tin nhắn
@router.get("/conversations/messages/search")
async def search_messages(
    conversation_id: str,
    query: str = None,
    start_date: str = None,
    end_date: str = None,
    current_user: dict = Depends(get_current_user)
):
    params = {"conversation_id": conversation_id}
    if query:
        params["query"] = query
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    return await forward_request(
        "GET", "conversations/messages/search",
        params=params,
        headers={"Authorization": f"Bearer {current_user['token']}"}
    )
