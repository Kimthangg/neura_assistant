"""
Utility module for MongoDB operations related to chat history
"""

import datetime

from pymongo import MongoClient

# from config.mongodb import COLLECTION_NAME, DB_NAME, MONGO_URI
import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
DB_NAME = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI")

class MongoDBManager:
    """
    Class to manage MongoDB operations for chat history
    """

    def __init__(self):
        """Initialize MongoDB connection"""
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            # Create index for chat_id for faster queries
            self.collection.create_index("chat_id")
            print(f"Kết nối MongoDB thành công")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None
            self.collection = None

    def save_chat_history(self, chat_id, chat_history, conversation_name=None):
        """
        Save chat history to MongoDB

        Args:
            chat_id (str): Unique identifier for the chat
            chat_history (list): List of chat messages
            conversation_name (str, optional): Name for this conversation

        Returns:
            bool: True if successful, False otherwise
        """
        if self.collection is None:
            print("MongoDB connection not available")
            return False

        try:
            # Generate conversation name if not provided
            if conversation_name is None and chat_history:
                # Use first user message as conversation name (truncate if too long)
                for msg in chat_history:
                    if msg.get("type") == "user":
                        conversation_name = msg.get("content", "")[:50]
                        if len(conversation_name) >= 50:
                            conversation_name += "..."
                        break

                # If still None (no user messages found), use timestamp
                if not conversation_name:
                    conversation_name = f"Hội thoại {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"

            # First check if history exists for this chat
            existing = self.collection.find_one({"chat_id": chat_id})

            if existing:
                # Update existing record
                result = self.collection.update_one(
                    {"chat_id": chat_id},
                    {
                        "$set": {
                            "chat_history": chat_history,
                            "conversation_name": conversation_name,
                            "updated_at": datetime.datetime.utcnow(),
                        }
                    },
                )
                success = result.modified_count > 0
                if success:
                    print(f"Đã cập nhật lịch sử chat cho chat_id: {chat_id}")
                return success
            else:
                # Create new record
                result = self.collection.insert_one(
                    {
                        "chat_id": chat_id,
                        "chat_history": chat_history,
                        "conversation_name": conversation_name,
                        "created_at": datetime.datetime.utcnow(),
                        "updated_at": datetime.datetime.utcnow(),
                    }
                )
                success = result.inserted_id is not None
                if success:
                    print(f"Đã tạo mới lịch sử chat cho chat_id: {chat_id}")
                return success

        except Exception as e:
            print(f"Lỗi khi lưu lịch sử chat: {e}")
            return False

    def load_chat_history(self, chat_id):
        """
        Load chat history from MongoDB

        Args:
            chat_id (str): Unique identifier for the chat

        Returns:
            list: Chat history if found, empty list otherwise
        """
        if self.collection is None:
            print("MongoDB connection not available")
            return []

        try:
            result = self.collection.find_one({"chat_id": chat_id})
            if result and "chat_history" in result:
                print(f"Đã tải lịch sử chat cho chat_id: {chat_id}")
                return result["chat_history"]
            print(f"Không tìm thấy lịch sử chat cho chat_id: {chat_id}")
            return []
        except Exception as e:
            print(f"Lỗi khi tải lịch sử chat: {e}")
            return []

    def delete_chat_history(self, chat_id):
        """
        Delete chat history for a chat

        Args:
            chat_id (str): Unique identifier for the chat

        Returns:
            bool: True if successful, False otherwise
        """
        if self.collection is None:
            print("MongoDB connection not available")
            return False

        try:
            result = self.collection.delete_one({"chat_id": chat_id})
            success = result.deleted_count > 0
            if success:
                print(f"Đã xóa lịch sử chat cho chat_id: {chat_id}")
            return success
        except Exception as e:
            print(f"Lỗi khi xóa lịch sử chat: {e}")
            return False

    def get_all_conversations(self):
        """
        Get all saved conversations from the database

        Returns:
            list: List of conversation records with chat_id, conversation_name, and updated_at
        """
        if self.collection is None:
            print("MongoDB connection not available")
            return []

        try:
            # Get all conversations with selected fields only
            conversations = list(
                self.collection.find(
                    {},
                    {"chat_id": 1, "conversation_name": 1, "updated_at": 1, "_id": 0},
                )
            )

            # Sort by updated_at (most recent first)
            conversations.sort(
                key=lambda x: x.get("updated_at", datetime.datetime.min), reverse=True
            )

            return conversations
        except Exception as e:
            print(f"Error getting conversation list: {e}")
            return []

    def close(self):
        """Close MongoDB connection"""
        if self.client is not None:
            self.client.close()
