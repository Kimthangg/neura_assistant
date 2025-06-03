import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import warnings
import pytest
warnings.filterwarnings("ignore")
import time
from features import tool_update_event, system_prompt_update_event
from services.llm.llm_config import LLM
from utils import *
# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")
weekdays = get_weekdays_context()

@pytest.fixture(scope="module")
def llm_extraction():
    return LLM(
        system_message=system_prompt_update_event,
        tool=tool_update_event,
        temperature=0.1
    )

@pytest.mark.parametrize("prompt, event_id, update_field, update_value",[
    # Cập nhật thời gian
    ("Dời cuộc họp có ID 12345 sang 15:00 ngày mai.", "12345", "time", "15:00:00"),
    ("Thay đổi thời gian buổi họp ID abc123 sang 10:00 sáng ngày 15 tháng 6.", "abc123", "time", "10:00:00"),
    ("Chuyển sự kiện ID event123 sang thứ Hai tuần tới.", "event123", "date", weekdays[7].strftime("%Y-%m-%d")),
    
    # Cập nhật thời lượng
    ("Kéo dài cuộc họp ID 12345 thành 2 tiếng.", "12345", "duration", "02:00:00"),
    ("Rút ngắn sự kiện ID abc123 xuống còn 30 phút.", "abc123", "duration", "00:30:00"),
    ("Thay đổi thời lượng của cuộc họp ID meeting123 thành 1 tiếng rưỡi.", "meeting123", "duration", "01:30:00"),
    
    # Cập nhật tiêu đề
    ("Đổi tên sự kiện ID 12345 thành 'Họp nhóm dự án X'.", "12345", "title", "Họp nhóm dự án X"),
    ("Thay đổi tiêu đề của lịch ID abc123 thành 'Gặp khách hàng mới'.", "abc123", "title", "Gặp khách hàng mới"),
    ("Cập nhật tên cuộc họp ID meeting123 thành 'Thảo luận kế hoạch quý 3'.", "meeting123", "title", "Thảo luận kế hoạch quý 3"),
    
    # Cập nhật địa điểm
    ("Thay đổi địa điểm cuộc họp ID 12345 thành 'Phòng họp A'.", "12345", "location", "Phòng họp A"),
    ("Cập nhật địa điểm sự kiện ID abc123 sang 'Nhà hàng Sen Tây Hồ'.", "abc123", "location", "Nhà hàng Sen Tây Hồ"),
    ("Chuyển địa điểm buổi gặp ID meeting123 đến 'Văn phòng chi nhánh quận 1'.", "meeting123", "location", "Văn phòng chi nhánh quận 1"),
    
    # Cập nhật mô tả
    ("Thêm mô tả cho sự kiện ID 12345: 'Chuẩn bị slide thuyết trình'.", "12345", "description", "Chuẩn bị slide thuyết trình"),
    ("Cập nhật thông tin chi tiết cho lịch ID abc123: 'Mang theo laptop và tài liệu'.", "abc123", "description", "Mang theo laptop và tài liệu"),
    ("Thay đổi mô tả cuộc họp ID meeting123 thành 'Thảo luận về các vấn đề phát sinh'.", "meeting123", "description", "Thảo luận về các vấn đề phát sinh"),
    
    # Cập nhật nhiều trường
    ("Thay đổi thời gian và địa điểm cuộc họp ID 12345 thành 16:00 tại Phòng họp B.", "12345", "time_location", ["16:00:00", "Phòng họp B"]),
    ("Cập nhật tiêu đề và thời lượng sự kiện ID abc123 thành 'Họp báo cáo' và kéo dài 45 phút.", "abc123", "title_duration", ["Họp báo cáo", "00:45:00"]),
    ("Dời cuộc họp ID meeting123 sang 14:00 ngày mai và đổi tên thành 'Họp khẩn'.", "meeting123", "time_title", ["14:00:00", "Họp khẩn"]),
],)

def test_update_event(llm_extraction, prompt, event_id, update_field, update_value):
    result = llm_extraction(prompt)
    event_update = result["event_update"]
    
    today_str = today.strftime("%Y-%m-%d")
    id_assertion = event_id in event_update.get("event_id", "")
    
    # Kiểm tra cập nhật dựa trên loại trường
    if update_field == "time":
        field_assertion = update_value in event_update.get("time", "")
    elif update_field == "date":
        field_assertion = update_value in event_update.get("date", "")
    elif update_field == "duration":
        field_assertion = update_value in event_update.get("duration", "")
    elif update_field == "title":
        field_assertion = update_value in event_update.get("title", "")
    elif update_field == "location":
        field_assertion = update_value in event_update.get("location", "")
    elif update_field == "description":
        field_assertion = update_value in event_update.get("description", "")
    elif update_field == "time_location":
        field_assertion = update_value[0] in event_update.get("time", "") and update_value[1] in event_update.get("location", "")
    elif update_field == "title_duration":
        field_assertion = update_value[0] in event_update.get("title", "") and update_value[1] in event_update.get("duration", "")
    elif update_field == "time_title":
        field_assertion = update_value[0] in event_update.get("time", "") and update_value[1] in event_update.get("title", "")
    else:
        field_assertion = False
    
    error_file = f"log/update_event_{today_str}.txt"
    if not id_assertion or not field_assertion:
        with open(error_file, "a", encoding="utf-8") as f:
            if not id_assertion:
                f.write(f"Event ID mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{event_id}'\n")
                f.write(f"  GenAI: '{event_update.get('event_id', '')}'\n\n")
            if not field_assertion:
                f.write(f"Update field mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{update_field}' with value '{update_value}'\n")
                f.write(f"  GenAI result: {event_update}\n\n")
    
    assert id_assertion, f"Failed for input '{prompt}'. Mong muốn ID '{event_id}' in GenAI '{event_update.get('event_id', '')}'"
    assert field_assertion, f"Failed for input '{prompt}'. Mong muốn '{update_field}' with value '{update_value}' không khớp với GenAI"
    time.sleep(4)

if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/calendar/update_event.py"])
