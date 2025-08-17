from utils.helpers import get_context_date

def get_scheduler_prompt():
    return """
    Trích xuất thông tin từ yêu cầu của người dùng về lên lịch thực hiện tác vụ tự động.
    
    Bạn cần phân tích và trích xuất các thông tin sau:
    1. Tên tác vụ (task_name): Mô tả lại chính xác tác vụ để agent khác có thể hiểu. Đưa các câu lặp lại thành chỉ lần đầu tiên.
    ví dụ: "Tóm tắt email hàng ngày" -> "Tóm tắt email hôm nay"
    
    2. Thời gian (time): Thời gian thực hiện tác vụ với các thành phần:
       - month: tháng thực hiện tác vụ (1-12)
       - day: ngày thực hiện tác vụ (1-31)
       - day_of_week: ngày trong tuần (0-6 hoặc mon-sun, ví dụ: 'mon', 'fri')
       - hour: giờ thực hiện tác vụ (0-23)
       - minute: phút thực hiện tác vụ (0-59)
       
       Lưu ý:
       - Nếu chỉ nói giờ không nói phút (ví dụ: 17h), sử dụng 0 cho phút
       - Nếu sử dụng kiểu 5h chiều, chuyển thành 17 giờ
       - Nếu không nhắc đến ngày cụ thể, sử dụng ngày hiện tại
       - Nếu nói "mỗi ngày", chỉ cần điền giờ và phút, các trường khác có thể bỏ trống
       - Nếu nói về ngày trong tuần (thứ 2, thứ 5...), điền vào trường day_of_week
   

    Ví dụ: 
    -Input: "Lên lịch tóm tắt email lúc 17h mỗi ngày"
    -Output:
    {
      "task_name": "Yêu cầu của người dùng: 'tóm tắt email hôm nay'",
      "time": {
        "hour": 17,
        "minute": 0,
      },
    }
    
    -Input: "Lên lịch tạo báo cáo tổng hợp về các cuộc họp hoặc sự kiện trong tuần tới vào 18h Chủ nhật"
    -Output:
    {
      "task_name": "Yêu cầu của người dùng: 'tạo báo cáo tổng hợp về các cuộc họp hoặc sự kiện trong tuần tới'",
      "time": {
        "day_of_week": "sun",
        "hour": 18,
        "minute": 0,
      },
    }
    
    -Input: "Lên lịch tóm tắt email vào ngày 25/12/2025 lúc 9h30"
    -Output:
    {
      "task_name": "Yêu cầu của người dùng: 'tóm tắt email vào ngày 25/12/2025 lúc 9h30'",
      "time": {
        "year": 2025,
        "month": 12,
        "day": 25,
        "hour": 9,
        "minute": 30,
      },
    }

    -Input: "Hủy lịch tóm tắt email hàng ngày lúc 17h"
    -Output:
    {
      "task_name": "Yêu cầu của người dùng: 'tóm tắt email hàng ngày lúc 17h'",
      "time": {
        "hour": 17,
        "minute": 0
      },
    }
    """