from typing import Dict, List

from bot.agent_calendar.get_event.prompt_get_event import get_calendar_rules
from services.llm.llm_config import LLM
from utils import get_context_date

tool_get_event = {
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
        "required": ["datetime_ranges","incorrect_datetime",],
    },
}

system_prompt_get_event = f"""Extract datetime ranges from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Xác thực xem câu lệnh có hợp lệ hay không, nếu không hợp lệ thì trả về incorrect_datetime là true.
        2. Tìm thời gian(ngày, tháng, năm ) chính xác và chuyển thành định dạng ISO (YYYY-MM-DD HH:mm:ss).
        3. Sau khi có đủ dữ liệu, hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
    - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
    - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    {get_calendar_rules}
    """


def get_event_extraction(text: str) -> Dict[str, List[Dict[str, str]]]:

    llm = LLM(system_prompt_get_event, tool_get_event, temperature=0.1)

    response = llm(text)
    return {**response}
