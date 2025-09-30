tool_summarize_emails = {
    "name": "extract_datetime",
    "description": """Extract start date and end date information from text.
    The function analyzes natural language to identify date and time references and returns them in a structured format.
    It should handle various date formats, relative dates (today, tomorrow,...), and time ranges.""",
    "parameters": {
        "type": "object",
        "properties": {
            "sender": {
                "type": "string",
                "description": "Người gửi email, ví dụ: boss@gmail.com hoặc chỉ cần tên như 'Bảo Ngọc'"
            },
            "start_date": {
                "type": "string",
                "description": "The start date in ISO format (YYYY-MM-DD) or '' if not specified"
            },
            "end_date": {
                "type": "string",
                "description": "The end date in ISO format (YYYY-MM-DD) or '' if not specified"
            },
            "incorrect_datetime": {
                "type": "boolean",
                "description": "Flag indicating if the provided date information is invalid or could not be parsed"
            }
        },
        "required": ["start_date", "end_date", "incorrect_datetime"]
    }
}
from utils.helpers import get_context_date
from .prompt import prompt_summarize_emails
system_prompt_summarize_emails = f"""Extract datetime ranges from the user's message.
    Hãy suy nghĩ từng bước trước khi trích xuất thông tin:
        1. Xác thực xem câu lệnh có hợp lệ hay không, nếu không hợp lệ thì trả về incorrect_datetime là true.
        2. Tìm thời gian(ngày, tháng, năm) chính xác và chuyển thành định dạng ISO (YYYY-MM-DD).
        3. Sau khi có đủ dữ liệu, hãy gọi function extract_datetime để trả về JSON.
    LƯU Ý QUAN TRỌNG:
    - Bạn PHẢI LUÔN LUÔN trả về dữ liệu theo định dạng yêu cầu
    - Không bao giờ được trả về null hoặc bỏ qua trường dữ liệu bắt buộc
    {get_context_date()}
    {prompt_summarize_emails()}
    """