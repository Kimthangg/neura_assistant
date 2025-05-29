tool_search_emails = {
    "name": "search_email",
    "description": "Tìm email theo thông tin người gửi, tiêu đề, thời gian và từ khóa",
    "parameters": {
        "type": "object",
        "properties": {
        "from": {
            "type": "string",
            "description": "Người gửi email, ví dụ: boss@gmail.com hoặc chỉ cần tên như 'Bảo Ngọc'"
        },
        "subject": {
            "type": "string",
            "description": "Tiêu đề email hoặc từ khóa trong tiêu đề, ví dụ: 'Báo cáo tháng 4'"
        },
        "keyword": {
            "type": "string",
            "description": "Từ khóa cần tìm trong nội dung email, ví dụ: 'báo cáo quý'"
        },
        "start_date": {
            "type": "string",
            "description": "Ngày bắt đầu tìm kiếm, định dạng YYYY/MM/DD"
        },
        "end_date": {
            "type": "string",
            "description": "Ngày kết thúc tìm kiếm, định dạng YYYY/MM/DD"
        },

        },
        "required": ["start_date", "end_date"],
    }
}
prompt_search_emails = """Bạn là một trợ lý ảo thông minh có khả năng tìm kiếm email theo các tiêu chí cụ thể.
"""


