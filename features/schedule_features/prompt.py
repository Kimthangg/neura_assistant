from utils import get_context_date

def get_scheduler_prompt():
    return """
    Trích xuất thông tin từ yêu cầu của người dùng về lên lịch thực hiện tác vụ tự động.
    
    Bạn cần phân tích và trích xuất các thông tin sau:
    1. Loại tác vụ (task_type): Xác định người dùng muốn lên lịch làm gì
       - summarize_emails: tóm tắt email
       - Các loại khác sẽ được hỗ trợ sau
    
    2. Tên tác vụ (task_name): Mô tả lại chính xác tác vụ để agent khác có thể hiểu
    
    3. Thời gian (time): Thời gian thực hiện tác vụ, định dạng HH:MM
       - Nếu chỉ nói giờ không nói phút (ví dụ: 17h), sử dụng 00 cho phút (17:00)
       - Nếu sử dụng kiểu 5h chiều, chuyển thành 17:00
    
    4. Hành động (action): Xác định người dùng muốn làm gì với lịch
       - schedule: lên lịch mới
       - cancel: hủy lịch đã có
       - list: liệt kê tất cả lịch

    
    Trả về JSON với cấu trúc:
    {
      "task_type": "summarize_emails",
      "task_name": "tóm tắt email",
      "time": "17:00",
      "action": "schedule"
    }
    Ví dụ: 
    -Input: "Lên lịch tóm tắt email lúc 17h mỗi ngày"
    -Output:
    {
      "task_type": "summarize_emails",
      "task_name": "tóm tắt email hôm nay",
      "time": "17:00",
      "action": "schedule"
    }
    """