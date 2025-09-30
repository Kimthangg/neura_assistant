"""
Base MongoDB Manager with common functionality
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
DB_NAME = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI")

class BaseMongoDBManager:
    """
    Base class to manage MongoDB operations
    """

    def __init__(self):
        """Initialize MongoDB connection"""
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            print(f"Kết nối MongoDB thành công")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None

    def close(self):
        """Close MongoDB connection"""
        if self.client is not None:
            self.client.close()


# Import managers (placed at the end to avoid circular imports)
from .chat_manager import ChatMongoDBManager
from .user_memory_manager import UserMemoryMongoDBManager

# For backward compatibility
class MongoDBManager(ChatMongoDBManager, UserMemoryMongoDBManager):
    """
    Combined MongoDB Manager that inherits from all specialized managers
    for backward compatibility
    """
    def __init__(self):
        """Initialize MongoDB connection once for all managers"""
        BaseMongoDBManager.__init__(self)
        # Initialize collection for chat manager
        if self.db is not None:
            self.collection = self.db[COLLECTION_NAME]
            # Create index for chat_id for faster queries
            self.collection.create_index("chat_id")
