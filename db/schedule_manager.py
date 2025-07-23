"""
Schedule task MongoDB operations
"""
import datetime
from .base_manager import BaseMongoDBManager

class ScheduleMongoDBManager(BaseMongoDBManager):
    """
    Class to manage MongoDB operations for scheduled tasks
    """

    def __init__(self):
        """Initialize MongoDB connection for schedule operations"""
        super().__init__()

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
