from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.triggers.cron import CronTrigger
import json
import pytz

from services.llm.llm_config import LLM
# from ..gmail_features import summarize_emails_apiz
from .agent_gmail import agent_gmail_executor_func
# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_jobstore(MemoryJobStore(), 'default')
scheduler.start()
from features.schedule_features.tools import tool_scheduler,system_prompt_scheduler
# Dictionary to keep track of scheduled jobs
scheduled_jobs = {}
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
    
    # Remove any existing job with the same ID
    if job_id in scheduled_jobs:
        scheduler.remove_job(scheduled_jobs[job_id])
    
    # Define the function to execute based on task_type
    if task_type == 'summarize_emails':
        job_func = lambda: agent_gmail_executor_func(task_name)
    else:
        return {"error": "Unsupported task type"}
    
    # Schedule the job
    job = scheduler.add_job(
        job_func,
        trigger=CronTrigger(hour=hour, minute=minute),
        id=job_id,
        replace_existing=True
    )
    
    scheduled_jobs[job_id] = job.id
    
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
    else:
        # Find all jobs matching the task_name and task_type
        matching_jobs = [job_id for job_id in scheduled_jobs.keys() 
                        if job_id.startswith(f"{task_type}_{task_name}_")]
        
        if not matching_jobs:
            return {"error": f"Không tìm thấy lịch {task_name} nào"}
        
        job_id = matching_jobs[0]  # Cancel the first matching job
    
    # Check if job exists
    if job_id in scheduled_jobs:
        scheduler.remove_job(scheduled_jobs[job_id])
        del scheduled_jobs[job_id]
        return {
            "success": True,
            "message": f"Đã hủy lịch {task_name}"
        }
    else:
        return {"error": f"Không tìm thấy lịch với ID {job_id}"}
def list_scheduled_tasks(args=None):
    """List all scheduled tasks"""
    if not scheduled_jobs:
        return {"message": "Không có lịch nào được thiết lập"}
    
    jobs_info = []
    for job_id in scheduled_jobs:
        job = scheduler.get_job(scheduled_jobs[job_id])
        if job:
            parts = job_id.split('_')
            task_type = parts[0]
            task_name = '_'.join(parts[1:-2])
            time = f"{parts[-2]}:{parts[-1]}"
            
            next_run = job.next_run_time.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
            next_run_str = next_run.strftime("%Y-%m-%d %H:%M:%S")
            
            jobs_info.append({
                "task_type": task_type,
                "task_name": task_name,
                "time": time,
                "next_run": next_run_str
            })
    
    return {"scheduled_tasks": jobs_info}
