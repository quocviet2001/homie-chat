from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from ..database import conversations_collection, messages_collection
from ..models.conversation import Conversation, Message
from ..middlewares.auth import get_current_user
from dateutil.parser import parse
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/conversations", tags=["Conversations"])

# Định nghĩa schema cho tạo hộp thoại
class ConversationCreate(BaseModel):
    friend_id: str

# Tạo hộp thoại mới
@router.post("", response_model=Conversation)
async def create_conversation(conversation: ConversationCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id") or current_user.get("id") 
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user data")
    
    existing_conversation = conversations_collection.find_one({
        "user_ids": {"$all": [user_id, conversation.friend_id], "$size": 2}
    })
    
    if existing_conversation:
        return Conversation(
            _id=str(existing_conversation["_id"]),
            user_ids=existing_conversation["user_ids"],
            created_at=existing_conversation["created_at"]
        )
    
    conversation_data = {
        "user_ids": [user_id, conversation.friend_id],
        "created_at": datetime.utcnow()
    }
    result = conversations_collection.insert_one(conversation_data)
    
    return Conversation(
        _id=str(result.inserted_id),
        user_ids=conversation_data["user_ids"],
        created_at=conversation_data["created_at"]
    )

# Lấy danh sách hộp thoại của người dùng
@router.get("", response_model=List[Conversation])
async def get_conversations(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["user_id"])  

    conversations = conversations_collection.find({"user_ids": user_id})
    converted_conversations = []
    
    for conv in conversations:
        try:
            converted_conversations.append({
                "_id": str(conv["_id"]),
                "user_ids": conv["user_ids"],
                "created_at": conv["created_at"]
            })
        except KeyError as e:
            print(f"Invalid conversation data: missing {e}")
            continue
    
    if not converted_conversations:
        return []
    
    return [Conversation(**conv) for conv in converted_conversations]


# Lấy lịch sử tin nhắn của hộp thoại
@router.get("/{conversation_id}/messages", response_model=List[Message])
async def get_messages(conversation_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]

    conversation = conversations_collection.find_one({
        "_id": ObjectId(conversation_id),
        "user_ids": user_id
    })
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")

    messages = messages_collection.find({"conversation_id": ObjectId(conversation_id)})
    converted_messages = [
        {**msg, "_id": str(msg["_id"]), "conversation_id": str(msg["conversation_id"])} for msg in messages
    ]
    return [Message(**msg) for msg in converted_messages]


# Tìm kiếm tin nhắn
@router.get("/messages/search", response_model=List[Message])
async def search_messages(
    conversation_id: str,
    query: str = None,
    start_date: str = None,
    end_date: str = None,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    conversation = conversations_collection.find_one({
        "_id": ObjectId(conversation_id),
        "user_ids": user_id
    })
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")

    search_query = {"conversation_id": ObjectId(conversation_id)}

    if query:
        search_query["content"] = {"$regex": query, "$options": "i"}  # Không phân biệt hoa thường

    if start_date and end_date:
        search_query["timestamp"] = {
            "$gte": parse(start_date),
            "$lte": parse(end_date)
        }

    messages = messages_collection.find(search_query)
    converted_messages = [
        {**msg, "_id": str(msg["_id"]), "conversation_id": str(msg["conversation_id"])} for msg in messages
    ]
    return [Message(**msg) for msg in converted_messages]
