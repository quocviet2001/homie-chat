from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Schema cho hộp thoại
class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_ids: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Schema cho tin nhắn
class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    conversation_id: str  
    sender_id: str        
    content: str          
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
