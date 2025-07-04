from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_DB = os.getenv("MONGO_DB", "homiechat")

# Kết nối với MongoDB
try:
    client = MongoClient(f"mongodb://{MONGO_HOST}:27017")
    client.admin.command('ping')
    print("MongoDB connection successful")
except ConnectionFailure:
    print("MongoDB connection failed")

db = client[MONGO_DB]
conversations_collection = db["conversations"]
messages_collection = db["messages"]

conversations_collection.create_index("user_ids")
messages_collection.create_index("conversation_id")
messages_collection.create_index("content")
messages_collection.create_index("timestamp")