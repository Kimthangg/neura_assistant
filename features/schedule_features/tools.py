from utils.helpers import get_context_date
from .prompt import get_scheduler_prompt
system_prompt_scheduler = f"""Extract scheduler information from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Xác định loại tác vụ người dùng muốn lên lịch (tóm tắt email, v.v.)
        2. Xác định thời gian thực hiện tác vụ 
        3. Xác định hành động (lên lịch mới, hủy lịch, liệt kê lịch)
        5. Sau khi có đủ dữ liệu, hãy gọi function extract_scheduler_info để trả về JSON.
    
    LƯU Ý QUAN TRỌNG:
    - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
    - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    
    {get_context_date()}
    {get_scheduler_prompt()}
    """

tool_scheduler = {
    "name": "extract_scheduler_info",
    "description": "Extract scheduler information from text",
    "parameters": {
        "type": "object",
        "properties": {
        "time": {
            "type": "object",
            "properties": {
            "month": {
                "type": "integer",
                "description": "Month (1-12)"
            },
            "day": {
                "type": "integer",
                "description": "Day of month (1-31)"
            },
            "day_of_week": {
                "type": "string",
                "description": "Day of week (0-6 or mon-sun) ví dụ: 'mon', 'fri'"
            },
            "hour": {
                "type": "integer",
                "description": "Hour (0-23)"
            },
            "minute": {
                "type": "integer",
                "description": "Minute (0-59)"
            },
            }
        },
        "task_name": {
            "type": "string",
            "description": "Name of the task"
        },
        "action": {
            "type": "string",
            "enum": ["schedule", "cancel", "list"],
            "description": "Action to perform (schedule, cancel or list)"
        },
        },
        "required": [
            "task_name",
            "time",
            "action"
        ]
    }
    }
