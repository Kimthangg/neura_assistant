from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.triggers.cron import CronTrigger
import json
import pytz
from datetime import datetime

from services.llm.llm_config import LLM
# from .agent_gmail import agent_gmail_executor_func
from db import MongoDBManager
from .bot_telegram import run_telegram_bot
# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_jobstore(MemoryJobStore(), 'default')
scheduler.start()
from features.schedule_features.tools import tool_scheduler, system_prompt_scheduler

# Initialize MongoDB Manager
db_manager = MongoDBManager()

# Function to load scheduled jobs from database
def load_scheduled_jobs_from_db():
    try:
        # Get all scheduled jobs from the database
        jobs = db_manager.get_scheduled_jobs()
        
        # Restore each job to the scheduler
        for job in jobs:
            job_id = job['job_id']
            task_type = job['task_type']
            task_name = job['task_name']
            hour = int(job['hour'])
            minute = int(job['minute'])
            
            # Define the function to execute based on task_type
            if task_type == 'summarize_emails':
                job_func = lambda: run_telegram_bot(task_name)
            else:
                continue  # Skip unsupported task types
            
            # Schedule the job
            scheduler_job = scheduler.add_job(
                job_func,
                trigger=CronTrigger(hour=hour, minute=minute),
                id=job_id,
                replace_existing=True
            )
            
        print(f"Loaded {len(jobs)} scheduled jobs from database")
    except Exception as e:
        print(f"Error loading scheduled jobs from database: {e}")

# Load scheduled jobs when module is imported
load_scheduled_jobs_from_db()

# Add scheduler-related tools
def schedule_task(user_message):
    """Schedule a recurring task at a specified time"""
    args = LLM(system_prompt_scheduler, tool_scheduler, temperature=0.1)(user_message)
    print(f"Received args: {args}")
    task_name = args.get('task_name')
    time_str = args.get('time')
    task_type = args.get('task_type')
    
    # Parse time (expecting format like "17:00")
    hour, minute = map(int, time_str.split(':'))
    
    # Create a job ID
    job_id = f"{task_type}_{task_name}_{hour:02d}_{minute:02d}"
    
    # Check if job exists in database and remove if it does
    existing_job = db_manager.get_scheduled_job(job_id)
    if existing_job:
        scheduler.remove_job(job_id)
        db_manager.delete_scheduled_job(job_id)
    
    # Define the function to execute based on task_type
    if task_type == 'summarize_emails':
        job_func = lambda: run_telegram_bot(task_name)
    else:
        return {"error": "Unsupported task type"}
    
    # Schedule the job
    job = scheduler.add_job(
        job_func,
        trigger=CronTrigger(hour=hour, minute=minute),
        id=job_id,
        replace_existing=True
    )
    
    # Save job to database
    job_data = {
        'job_id': job_id,
        'task_type': task_type,
        'task_name': task_name,
        'hour': hour,
        'minute': minute,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    db_manager.save_scheduled_job(job_data)
    
    return {
        "success": True,
        "message": f"Đã lên lịch {task_name} vào lúc {hour:02d}:{minute:02d} hàng ngày",
        "job_id": job_id
    }

def cancel_scheduled_task(user_message):
    """Cancel a scheduled task"""
    args = LLM(system_prompt_scheduler, tool_scheduler, temperature=0.1)(user_message)
    print(f"Received args cancel: {args}")

    task_name = args.get('task_name')
    task_type = args.get('task_type')
    time_str = args.get('time')
    
    # Parse time if provided
    if time_str:
        hour, minute = map(int, time_str.split(':'))
        job_id = f"{task_type}_{task_name}_{hour:02d}_{minute:02d}"
        
        # Check if job exists
        if db_manager.get_scheduled_job(job_id):
            scheduler.remove_job(job_id)
            db_manager.delete_scheduled_job(job_id)
            return {
                "success": True,
                "message": f"Đã hủy lịch {task_name}"
            }
    else:
        # Find all jobs matching the task_name and task_type
        matching_jobs = db_manager.find_scheduled_jobs_by_task(task_type, task_name)
        
        if not matching_jobs:
            return {"error": f"Không tìm thấy lịch {task_name} nào"}
        
        job_data = matching_jobs[0]  # Cancel the first matching job
        job_id = job_data['job_id']
        
        # Remove job from scheduler and database
        scheduler.remove_job(job_id)
        db_manager.delete_scheduled_job(job_id)
        return {
            "success": True,
            "message": f"Đã hủy lịch {task_name}"
        }
    
    return {"error": f"Không tìm thấy lịch với ID {job_id}"}

def list_scheduled_tasks(args=None):
    """List all scheduled tasks"""
    jobs = db_manager.get_scheduled_jobs()
    
    if not jobs:
        return {"message": "Không có lịch nào được thiết lập"}
    
    jobs_info = []
    for job_data in jobs:
        job_id = job_data['job_id']
        scheduler_job = scheduler.get_job(job_id)
        
        if scheduler_job:
            next_run = scheduler_job.next_run_time.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
            next_run_str = next_run.strftime("%Y-%m-%d %H:%M:%S")
        else:
            next_run_str = "Không xác định"
        
        jobs_info.append({
            "task_type": job_data['task_type'],
            "task_name": job_data['task_name'],
            "time": f"{job_data['hour']:02d}:{job_data['minute']:02d}",
            "next_run": next_run_str
        })
    
    return {"scheduled_tasks": jobs_info}