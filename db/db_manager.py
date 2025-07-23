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
from services.embedding_model.embedding import embedding_text
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
            )            # Sort by updated_at (most recent first)
            conversations.sort(
                key=lambda x: x.get("updated_at", datetime.datetime.min), reverse=True
            )

            return conversations
        except Exception as e:
            print(f"Error getting conversation list: {e}")
            return []
    # ===== Gmail Summarization Methods =====        
    def save_summarized_emails(self, emails):
        """
        Save summarized emails to a separate collection in MongoDB
        
        Args:
            emails (list): List of email summary objects
                The only required field is 'id' for each email
                All other fields will be stored as provided

        Returns:
            bool: True if successful, False otherwise
        """
        if self.client is None:
            print("MongoDB connection not available")
            return False

        try:
            # Use a separate collection for summarized emails
            email_collection = self.db["summarized_emails"]
            
            # Create index for email_id for faster queries
            email_collection.create_index("id", unique=True)
            
            # Track success count
            success_count = 0
            
            for email in emails:
                print(email)
                # Ensure ID field exists
                if "id" not in email and "personal_data" not in email:
                    print(f"Thiếu trường ID bắt buộc trong email")
                    continue
                
                # Add timestamp for when this record was saved
                email_doc = email.copy()  # Create a copy to avoid modifying the original
                email_doc["saved_at"] = datetime.datetime.utcnow()
                # Create a text string from the email document for embedding
                data_embed = ""
                for key, value in email_doc.items():
                    if key not in ["id", "saved_at"] and value:  # Skip id and saved_at fields
                        data_embed += f"{key}: {value} "
                # Generate embedding for the combined text
                email_doc['embedding'] = embedding_text(data_embed)
                # Insert or update (upsert) the document
                result = email_collection.update_one(
                    {"id": email["id"]},
                    {"$set": email_doc},
                    upsert=True
                )
                
                if result.upserted_id or result.modified_count > 0:
                    success_count += 1
            
            print(f"Đã lưu {success_count}/{len(emails)} email tóm tắt vào cơ sở dữ liệu")
            return success_count > 0
            
        except Exception as e:
            print(f"Lỗi khi lưu email tóm tắt: {e}")
            return False
    
    def get_summarized_emails(self, email_ids):
        """
        Get summarized emails from MongoDB
        
        Args:
            limit (int): Maximum number of records to return
            skip (int): Number of records to skip (for pagination)
            sort_by (str): Field to sort by (default: time)
            sort_order (int): Sort order (1 for ascending, -1 for descending)
            
        Returns:
            list: List of summarized email records
        """
        if self.client is None:
            print("MongoDB connection not available")
            return []
            
        try:
            email_collection = self.db["summarized_emails"]
            
            # Get emails with pagination and sorting
            emails = list(
                email_collection.find(
                    {"id": {"$in": email_ids}},
                    {"_id": 0, # Exclude MongoDB ID
                     "embedding": 0}  # Exclude embedding field
                )
            )
            
            return emails
        except Exception as e:
            print(f"Lỗi khi lấy danh sách email tóm tắt: {e}")
            return []
    def search_emails_by_vector(self, query_text, limit=5):
        """
        Search emails using vector similarity search
        
        Args:
            query_text (str): The query text to search for
            limit (int, optional): Maximum number of results to return. Defaults to 5.
            
        Returns:
            list: List of matching email documents
        """
        if self.client is None:
            print("MongoDB connection not available")
            return []
            
        try:
            # Generate embedding for the query text
            query_vector = embedding_text(query_text)
            
            # Use MongoDB's vector search aggregation
            email_collection = self.db["summarized_emails"]
            
            # Run the aggregation pipeline with vector search
            results = email_collection.aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": 100,
                        "limit": limit,
                        "similarity": "cosine"
                    }
                },
                {
                    "$project": {
                        "score": { "$meta": "vectorSearchScore" },
                        "embedding": 0
                    }
                },
                {
                    "$sort": {
                        "score": -1 # Sort by similarity score in descending order
                    }
                }
            ])
            
            # Convert results to a list
            matching_emails = list(results)
            
            # Remove MongoDB _id field from results
            for email in matching_emails:
                if "_id" in email:
                    del email["_id"]
                    
            return matching_emails
            
        except Exception as e:
            print(f"Lỗi khi tìm kiếm email theo vector: {e}")
            return []
    # ====== Schedule Task Methods ======
    # Add these methods to the MongoDBManager class

    def save_scheduled_job(self, job_data):
        """
        Save a scheduled job to the database
        
        Args:
            job_data (dict): Job data including job_id, task_type, task_name, hour, minute
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            collection = self.db["scheduled_jobs"]
            
            # Check if job already exists
            existing_job = collection.find_one({"job_id": job_data["job_id"]})
            
            if existing_job:
                # Update existing job
                job_data["updated_at"] = datetime.datetime.utcnow()
                result = collection.update_one(
                    {"job_id": job_data["job_id"]},
                    {"$set": job_data}
                )
                success = result.modified_count > 0
            else:
                # Insert new job
                result = collection.insert_one(job_data)
                success = result.inserted_id is not None
                
            if success:
                print(f"Đã lưu công việc lên lịch với ID: {job_data['job_id']}")
            return success
        except Exception as e:
            print(f"Lỗi khi lưu công việc lên lịch: {e}")
            return False

    def get_scheduled_job(self, job_id):
        """
        Get a scheduled job by ID
        
        Args:
            job_id (str): Job ID
            
        Returns:
            dict: Job data if found, None otherwise
        """
        try:
            collection = self.db["scheduled_jobs"]
            job = collection.find_one({"job_id": job_id})
            
            if job and "_id" in job:
                del job["_id"]
                
            return job
        except Exception as e:
            print(f"Lỗi khi lấy công việc lên lịch: {e}")
            return None

    def get_scheduled_jobs(self):
        """
        Get all scheduled jobs
        
        Returns:
            list: List of job data
        """
        try:
            collection = self.db["scheduled_jobs"]
            jobs = list(collection.find({}))
            
            # Remove MongoDB _id field from results
            for job in jobs:
                if "_id" in job:
                    del job["_id"]
                    
            return jobs
        except Exception as e:
            print(f"Lỗi khi lấy danh sách công việc lên lịch: {e}")
            return []

    def find_scheduled_jobs_by_task(self, task_type, task_name):
        """
        Find scheduled jobs by task type and name
        
        Args:
            task_type (str): Task type
            task_name (str): Task name
            
        Returns:
            list: List of matching job data
        """
        try:
            collection = self.db["scheduled_jobs"]
            query = {"task_type": task_type}
            
            if task_name:
                query["task_name"] = task_name
                
            jobs = list(collection.find(query))
            
            # Remove MongoDB _id field from results
            for job in jobs:
                if "_id" in job:
                    del job["_id"]
                    
            return jobs
        except Exception as e:
            print(f"Lỗi khi tìm kiếm công việc lên lịch: {e}")
            return []

    def delete_scheduled_job(self, job_id):
        """
        Delete a scheduled job by ID
        
        Args:
            job_id (str): Job ID
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            collection = self.db["scheduled_jobs"]
            result = collection.delete_one({"job_id": job_id})
            
            success = result.deleted_count > 0
            if success:
                print(f"Đã xóa công việc lên lịch với ID: {job_id}")
            return success
        except Exception as e:
            print(f"Lỗi khi xóa công việc lên lịch: {e}")
            return False
    def close(self):
        """Close MongoDB connection"""
        if self.client is not None:
            self.client.close()
