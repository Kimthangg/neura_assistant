"""
Email and user information MongoDB operations
"""
import datetime
from .base_manager import BaseMongoDBManager
from services.embedding_model.embedding import embedding_text

class UserMemoryMongoDBManager(BaseMongoDBManager):
    """
    MongoDB manager for handling email summaries and user information.
    
    This class provides operations for storing, retrieving, and searching email summaries
    and user profile data in MongoDB. It supports vector-based similarity search using
    embeddings for intelligent information retrieval.
    
    Collections used:
    - user_memory: Stores email summaries with embeddings
    - user_profile: Stores user personal information
    """

    def __init__(self):
        """Initialize MongoDB connection for email and user information operations."""
        super().__init__()

    def save_info(self, emails):
        """
        Save email summaries or user profile information to MongoDB.
        
        Automatically determines the collection based on data content:
        - If 'personal_data' field exists, saves to 'user_profile' collection
        - Otherwise, saves to 'user_memory' collection
        
        For each record:
        - Generates vector embeddings from text content
        - Adds timestamp metadata
        - Performs upsert operation (insert or update)
        
        Args:
            emails (list): List of data objects to save. Each object must have:
                - 'id' field (required): Unique identifier
                - Other fields will be stored as provided
        
        Returns:
            bool: True if at least one record was successfully saved, False otherwise
        """
        if self.client is None:
            print("MongoDB connection not available")
            return False

        try:
            collection = self.db["user_memory"]
            # Create index for email_id for faster queries
            collection.create_index("id", unique=True)

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
                result = collection.update_one(
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

    def get_info(self, email_ids):
        """
        Retrieve email summaries from MongoDB by their IDs.
        
        Fetches email records from the 'user_memory' collection,
        excluding internal MongoDB fields and embedding vectors for performance.
        
        Args:
            email_ids (list): List of email ID strings to retrieve
            
        Returns:
            list: List of email summary documents. Each document contains
                 all fields except '_id' and 'embedding'. Returns empty list
                 if no emails found or on error.
        """
        if self.client is None:
            print("MongoDB connection not available")
            return []
            
        try:
            email_collection = self.db["user_memory"]
            
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

    def search_info_by_vector(self, query_text, limit=5):
        """
        Perform vector similarity search on email summaries using natural language queries.
        
        Converts the query text to an embedding vector and searches for semantically
        similar email summaries using MongoDB's vector search capabilities.
        
        Requirements:
        - MongoDB Atlas with vector search index named 'vector_index' on 'embedding' field
        - Index must be configured for cosine similarity
        
        Args:
            query_text (str): Natural language query to search for
            limit (int, optional): Maximum number of results to return. Defaults to 5.
            
        Returns:
            list: List of matching email documents ordered by similarity score.
                 Each document includes a 'score' field indicating similarity.
                 Returns empty list if no matches found or on error.
                 
        Example:
            results = manager.search_info_by_vector("meeting next week", limit=3)
            for email in results:
                print(f"Score: {email['score']}, Subject: {email.get('subject', '')}")
        """
        if self.client is None:
            print("MongoDB connection not available")
            return []
            
        try:
            # Generate embedding for the query text
            query_vector = embedding_text(query_text)
            
            # Use MongoDB's vector search aggregation
            email_collection = self.db["user_memory"]
            
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
