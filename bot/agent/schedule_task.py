from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.triggers.cron import CronTrigger

from services.llm.llm_config import LLM

# Initialize the scheduler
import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
# ================== INIT ==================
jobstores = {
    'default': MongoDBJobStore(
        database=DB_NAME,
        collection='scheduled_jobs',
        host=MONGO_URI
    )
}
scheduler = BackgroundScheduler(jobstores=jobstores, timezone="Asia/Ho_Chi_Minh")
scheduler.start()

from features.schedule_features.tools import tool_scheduler, system_prompt_scheduler
import json
# Use a wrapper function that imports run_telegram_bot when needed
def job_func_wrapper(task_name):
    from .bot_telegram import reponse_task_schedule
    import asyncio
    # Run the async function in the event loop
    asyncio.run(reponse_task_schedule(task_name))
def extract_time(time):
    print('Đang extract time.......................')
    time = json.loads(json.dumps(time))  
    hour = time.get('hour')
    minute = time.get('minute')
    day_of_week = time.get('day_of_week')
    month = time.get('month')
    day = time.get('day')
    # Nếu tất cả đều None
    if all(v is None for v in [day, month, hour, minute, day_of_week]):
        return "Không có thông tin thời gian nào được cung cấp, vui lòng cung cấp thời gian!"
    return day, month, hour, minute, day_of_week
# Add scheduler-related tools
def schedule_task(user_message):
    """Schedule a recurring task at a specified time"""
    args = LLM(system_prompt_scheduler, tool_scheduler, temperature=0.1)(user_message)
    print(f"Received args: {args}")
    task_name = args.get('task_name')
    time_json = args.get('time')
    
    day, month, hour, minute, day_of_week = extract_time(time_json)
    
    # Create a job ID
    job_id = f"{task_name}_{day or '*'}_{month or '*'}_{hour or '*'}_{minute or '*'}_{day_of_week or '*'}"

    # Xóa job cũ nếu tồn tại
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    
    # Schedule the job
    scheduler.add_job(
        job_func_wrapper,
        trigger=CronTrigger(day=day, month=month, day_of_week=day_of_week, hour=hour, minute=minute),
        id=job_id,
        args=[task_name],
        # kwargs={**time_json},
        replace_existing=True
    )
    
    return {
        "success": True,
        "message": f"Đã lên lịch {task_name}",
        "job_id": job_id
    }

def cancel_scheduled_task(user_message):
    """Cancel a scheduled task"""
    args = LLM(system_prompt_scheduler, tool_scheduler, temperature=0.1)(user_message)
    print(f"Received args cancel: {args}")

    task_name = args.get('task_name')
    time_json = args.get('time')
    
    day, month, hour, minute, day_of_week = extract_time(time_json)

    job_id = f"{task_name}_{day or '*'}_{month or '*'}_{hour or '*'}_{minute or '*'}_{day_of_week or '*'}"
    if not job_id:
        return {"error": f"Không tìm thấy lịch {task_name}"}
    scheduler.remove_job(job_id)

    return {"success": True, "message": f"Đã hủy lịch {task_name}"}

def list_scheduled_tasks(_=None):
    jobs = scheduler.get_jobs()
    if not jobs:
        return {"message": "Không có lịch nào được thiết lập"}

    jobs_info = []
    for job in jobs:
        next_run_str = (
            job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
            if job.next_run_time else "Không xác định"
        )
        jobs_info.append({
            "job_id": job.id,
            "task_name": job.name,
            "time": f"{job.trigger}",
            "next_run": next_run_str
        })
    return {"scheduled_tasks": jobs_info}
