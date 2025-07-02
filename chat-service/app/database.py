from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

MONGO_URI = os.getenv("MONGO_URI")

# Kết nối với MongoDB
try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("MongoDB connection successful")
except ConnectionFailure:
    print("MongoDB connection failed")

db = client["homie_chat"]
conversations_collection = db["conversations"]
messages_collection = db["messages"]

conversations_collection.create_index("user_ids")
messages_collection.create_index("conversation_id")
messages_collection.create_index("content")
messages_collection.create_index("timestamp")