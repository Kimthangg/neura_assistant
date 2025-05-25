from typing import Dict, List

from services.llm.llm_config import LLM
from utils import get_context_date

from .prompt_create_event import create_event_normal

tool_create_event = {
    "name": "extract_datetime_create_event",
    "description": "Extract information(title, datetime_ranges, incorrect_datetime, is_recurring, location, reminders) to create a normal event from text",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Title/name of the event (e.g., khám bệnh, cuộc họp, hội thảo, đi chơi, học Toeic, etc.)",
            },
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
                        "rrules": {
                            "type": "string",
                            "description": "Recurrence rules(formal iCalendar) if it's a recurring event (e.g., mỗi, hàng tuần, hàng tháng, etc.)",
                        },
                    },
                    "required": ["start_datetime", "end_datetime"],
                },
                "description": "List of datetime ranges extracted from the text",
            },
            "location": {"type": "string", "description": "Location of the event"},
            "incorrect_datetime": {
                "type": "boolean",
                "description": "True if there are invalid datetime patterns",
            },
            "reminders": {
                "type": "object",
                "description": "Reminder settings for the event",
                "properties": {
                    "usedefault": {
                        "type": "boolean",
                        "description": "Whether to use calendar's default reminders",
                    },
                    "overrides": {
                        "type": "array",
                        "description": "Custom reminder overrides",
                        "items": {
                            "type": "object",
                            "properties": {
                                "method": {
                                    "type": "string",
                                    "description": "Reminder method only popup",
                                },
                                "minutes": {
                                    "type": "integer",
                                    "description": "Number of minutes before the event",
                                },
                            },
                            "required": ["method", "minutes"],
                        },
                    },
                },
                "required": ["usedefault"],
            },
        },
    },
    "required": ["title", "datetime_ranges", "incorrect_datetime", "location"],
}

system_prompt_create_event = f"""Extract information to create an event from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Xác định tiêu đề/tên của sự kiện.
        2. Kiểm tra xem thông tin ngày giờ có hợp lệ hay không. Nếu không hợp lệ đặt incorrect_datetime = True.
        3. Tìm ngày giờ chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss) không được sử dụng ngày trong quá khứ.
        4. Xác định địa điểm diễn ra sự kiện nếu có
        5. Sau khi có đủ dữ liệu, hãy gọi function extract_datetime_create_event để trả về JSON.
    LƯU Ý QUAN TRỌNG:
    - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu không được trả về JSON rỗng
    - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    {create_event_normal()}"""


def create_event_extraction(text: str) -> Dict[str, List[Dict[str, str]]]:

    llm = LLM(system_prompt_create_event, tool_create_event, temperature=0.1)

    response = llm(text)
    return {**response}
