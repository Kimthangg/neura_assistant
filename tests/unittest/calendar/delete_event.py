import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import warnings
import pytest
warnings.filterwarnings("ignore")
import time
from features import tool_delete_event, system_prompt_delete_event
from services.llm.llm_config import LLM
from utils import *
# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")
weekdays = get_weekdays_context()

@pytest.fixture(scope="module")
def llm_extraction():
    return LLM(
        system_message=system_prompt_delete_event,
        tool=tool_delete_event,
        temperature=0.1
    )

@pytest.mark.parametrize("prompt, event_id, expected_action",[
    # Xóa sự kiện bằng ID
    ("Xóa sự kiện có ID 12345.", "12345", "delete"),
    ("Hủy lịch có mã abc123.", "abc123", "delete"),
    ("Xóa cuộc họp với ID meeting123.", "meeting123", "delete"),
    
    # Xóa sự kiện với xác nhận
    ("Tôi muốn xóa sự kiện có ID 12345, xác nhận xóa.", "12345", "delete_confirmed"),
    ("Hãy xóa lịch hẹn với mã abc123, tôi chắc chắn muốn xóa.", "abc123", "delete_confirmed"),
    ("Xóa cuộc họp ID meeting123, tôi đồng ý xóa nó.", "meeting123", "delete_confirmed"),
    
    # Xóa sự kiện vĩnh viễn
    ("Xóa vĩnh viễn sự kiện có ID 12345.", "12345", "delete_permanent"),
    ("Hủy hoàn toàn lịch có mã abc123.", "abc123", "delete_permanent"),
    ("Xóa vĩnh viễn cuộc họp với ID meeting123.", "meeting123", "delete_permanent"),
    
    # Xóa với thông tin bổ sung
    ("Xóa sự kiện ID 12345 vì tôi bận việc đột xuất.", "12345", "delete_with_reason"),
    ("Hủy lịch abc123 do thay đổi kế hoạch.", "abc123", "delete_with_reason"),
    ("Xóa cuộc họp ID meeting123 vì đã hoàn thành công việc sớm.", "meeting123", "delete_with_reason"),
    
    # Xóa sự kiện với yêu cầu thông báo
    ("Xóa sự kiện ID 12345 và thông báo cho người tham gia.", "12345", "delete_with_notification"),
    ("Hủy lịch abc123 và gửi email thông báo.", "abc123", "delete_with_notification"),
    ("Xóa cuộc họp ID meeting123 và cập nhật trạng thái cho nhóm.", "meeting123", "delete_with_notification"),
    
    # Xóa sự kiện lặp lại
    ("Xóa tất cả sự kiện lặp lại có ID 12345.", "12345", "delete_recurring"),
    ("Hủy chuỗi lịch có mã abc123.", "abc123", "delete_recurring"),
    ("Xóa toàn bộ cuộc họp định kỳ với ID meeting123.", "meeting123", "delete_recurring"),
    
    # Xóa một sự kiện trong chuỗi lặp lại
    ("Xóa chỉ sự kiện ngày mai trong chuỗi có ID 12345.", "12345", "delete_single_instance"),
    ("Hủy buổi họp ngày 15/06 trong lịch lặp lại có mã abc123.", "abc123", "delete_single_instance"),
    ("Xóa cuộc họp thứ Hai tuần này trong chuỗi định kỳ có ID meeting123.", "meeting123", "delete_single_instance"),
],)

def test_delete_event(llm_extraction, prompt, event_id, expected_action):
    result = llm_extraction(prompt)
    event_deletion = result["event_deletion"]
    
    today_str = today.strftime("%Y-%m-%d")
    id_assertion = event_id in event_deletion.get("event_id", "")
    action_assertion = expected_action in event_deletion.get("action", "")
    
    error_file = f"log/delete_event_{today_str}.txt"
    if not id_assertion or not action_assertion:
        with open(error_file, "a", encoding="utf-8") as f:
            if not id_assertion:
                f.write(f"Event ID mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{event_id}'\n")
                f.write(f"  GenAI: '{event_deletion.get('event_id', '')}'\n\n")
            if not action_assertion:
                f.write(f"Action mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_action}'\n")
                f.write(f"  GenAI: '{event_deletion.get('action', '')}'\n\n")
    
    assert id_assertion, f"Failed for input '{prompt}'. Mong muốn ID '{event_id}' in GenAI '{event_deletion.get('event_id', '')}'"
    assert action_assertion, f"Failed for input '{prompt}'. Mong muốn action '{expected_action}' in GenAI '{event_deletion.get('action', '')}'"
    time.sleep(4)

if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/calendar/delete_event.py"])
