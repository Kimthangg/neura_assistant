from typing import Dict, List

from bot.agent_calendar.update_event.prompt_update_event import update_calendar_rules
from services.llm.llm_config import LLM
from utils import get_context_date

tool_update_event = {
    "name": "extract_datetime",
    "description": "Extract datetime ranges, title, and location from text",
    "parameters": {
        "type": "object",
        "properties": {
            "title_old": {
                "type": "string",
                "description": "Original title/name of the event before the update",
            },
            "title_new": {
                "type": "string",
                "description": "Updated title/name of the event (e.g., khám bệnh, cuộc họp, hội thảo, đi chơi, học Toeic, etc.)",
            },
            "location_old": {
                "type": "string",
                "description": "Original location of the event before the update",
            },
            "location_new": {
                "type": "string",
                "description": "Updated location of the event",
            },
            "datetime_ranges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "start_datetime": {
                            "type": "string",
                            "description": "Original start datetime before the update, in ISO format (YYYY-MM-DD HH:mm:ss)",
                        },
                        "end_datetime": {
                            "type": "string",
                            "description": "Original end datetime before the update, in ISO format (YYYY-MM-DD HH:mm:ss)",
                        },
                        "start_new": {
                            "type": "string",
                            "description": "Updated start datetime after the change, in ISO format (YYYY-MM-DD HH:mm:ss)",
                        },
                        "end_new": {
                            "type": "string",
                            "description": "Updated end datetime after the change, in ISO format (YYYY-MM-DD HH:mm:ss)",
                        },
                    },
                    "required": [
                        "start_datetime",
                        "end_datetime",
                        "start_new",
                        "end_new",
                    ],
                },
                "description": "List of datetime ranges extracted from the text",
            },
            "incorrect_datetime": {
                "type": "boolean",
                "description": "True if there are invalid datetime patterns",
            },
        },
        "required": [
            "datetime_ranges",
            "incorrect_datetime",
            "title_old",
            "title_new",
            "location_old",
            "location_new",
        ],
    },
}

system_prompt_update_event = f"""Extract datetime ranges, title, and location from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Trích xuất tiêu đề/tên sự kiện cũ nếu được đề cập trong tin nhắn.
        2. Trích xuất tiêu đề/tên sự kiện mới nếu được đề cập trong tin nhắn.
        3. Trích xuất địa điểm cũ nếu được đề cập trong tin nhắn.
        4. Trích xuất địa điểm mới nếu được đề cập trong tin nhắn.
        5. Tìm ngày giờ cũ và mới chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss).
        6. Sau khi có đủ dữ liệu, hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
        - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
        - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
        - Nếu không tìm thấy thông tin title hoặc location, hãy để trống ('')
    {get_context_date()}
    {update_calendar_rules}
    """


def update_event_extraction(text: str) -> Dict[str, List[Dict[str, str]]]:

    llm = LLM(system_prompt_update_event, tool_update_event, temperature=0.1)

    response = llm(text)
    return {**response}
    # print(response)
