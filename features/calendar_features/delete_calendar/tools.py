tool_delete_event = {
    "name": "extract_datetime",
    "description": "Extract datetime ranges from text",
    "parameters": {
        "type": "object",
        "properties": {
            "datetime_ranges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "start_datetime": {
                            "type": "string",
                            "description": "Start date and time in ISO format (YYYY-MM-DD HH:mm:ss)",
                        },
                        "end_datetime": {
                            "type": "string",
                            "description": "End date and time in ISO format (YYYY-MM-DD HH:mm:ss)",
                        },
                    },
                    "required": ["start_datetime", "end_datetime"],
                },
                "description": "List of datetime ranges extracted from the text",
            },
            "incorrect_datetime": {
                "type": "boolean",
                "description": "True if there are invalid datetime patterns",
            },
        },
        "required": ["incorrect_datetime", "datetime_ranges"],
    },
}

from utils import get_context_date
from .prompt import delete_event_rules
system_prompt_delete_event = f"""Extract datetime ranges from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Tìm ngày giờ chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss).
        2. Sau đó hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
        - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
        - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    {delete_event_rules}
    """