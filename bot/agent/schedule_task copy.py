from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.triggers.cron import CronTrigger
import asyncio

from services.llm.llm_config import LLM
from features.schedule_features.tools import tool_scheduler, system_prompt_scheduler

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


# ================== HELPERS ==================
def make_job_id(task_type, task_name, hour, minute):
    return f"{task_type}_{task_name}_{hour:02d}_{minute:02d}"


def get_job_func(task_type, task_name):
    if task_type == "summarize_emails":
        def job_func_wrapper(task_name=task_name):
            from .bot_telegram import reponse_task_schedule
            asyncio.run(reponse_task_schedule(task_name))
        return job_func_wrapper
    return None


# ================== CORE ==================
def schedule_task(user_message):
    args = LLM(system_prompt_scheduler, tool_scheduler, temperature=0.1)(user_message)
    print(f"Received args: {args}")

    task_name = args.get("task_name")
    task_type = args.get("task_type")
    time_str = args.get("time")

    if not (task_name and task_type and time_str):
        return {"error": "Thiếu tham số (task_name, task_type, time)"}

    hour, minute = map(int, time_str.split(":"))
    job_id = make_job_id(task_type, task_name, hour, minute)

    # Xóa job cũ nếu tồn tại
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    job_func = get_job_func(task_type, task_name)
    if not job_func:
        return {"error": "Unsupported task type"}

    scheduler.add_job(
        job_func,
        trigger=CronTrigger(hour=hour, minute=minute),
        id=job_id,
        replace_existing=True
    )

    return {
        "success": True,
        "message": f"Đã lên lịch {task_name} vào {hour:02d}:{minute:02d} hàng ngày",
        "job_id": job_id
    }


def cancel_scheduled_task(user_message):
    args = LLM(system_prompt_scheduler, tool_scheduler, temperature=0.1)(user_message)
    print(f"Received args cancel: {args}")

    task_name, task_type, time_str = args.get("task_name"), args.get("task_type"), args.get("time")

    if not (task_name and task_type):
        return {"error": "Thiếu task_name hoặc task_type"}

    if time_str:
        hour, minute = map(int, time_str.split(":"))
        job_id = make_job_id(task_type, task_name, hour, minute)
        job = scheduler.get_job(job_id)
        if not job:
            return {"error": f"Không tìm thấy lịch {task_name}"}
        scheduler.remove_job(job_id)
    else:
        # Xóa tất cả jobs có task_name + task_type
        jobs = scheduler.get_jobs()
        jobs = [j for j in jobs if j.id.startswith(f"{task_type}_{task_name}")]
        if not jobs:
            return {"error": f"Không tìm thấy lịch {task_name}"}
        for j in jobs:
            scheduler.remove_job(j.id)

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
            "next_run": next_run_str
        })
    return {"scheduled_tasks": jobs_info}
