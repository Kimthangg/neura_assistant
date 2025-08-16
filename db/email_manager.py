"""
Email summarization MongoDB operations
"""
import datetime
from .base_manager import BaseMongoDBManager
from services.embedding_model.embedding import embedding_text

class EmailMongoDBManager(BaseMongoDBManager):
    """
    Class to manage MongoDB operations for email summarization
    """

    def __init__(self):
        """Initialize MongoDB connection for email operations"""
        super().__init__()

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
            if "personal_data" not in email:
                print(f"Đã lưu data người dùng vào cơ sở dữ liệu")
            else:
                print(f"Đã lưu {success_count}/{len(emails)} email tóm tắt vào cơ sở dữ liệu")
            return success_count > 0
            
        except Exception as e:
            print(f"Lỗi khi lưu email tóm tắt: {e}")
            return False
    
    def get_summarized_emails(self, email_ids):
        """
        Get summarized emails from MongoDB
        
        Args:
            email_ids (list): List of email IDs to retrieve
            
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
