import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import warnings
import pytest
warnings.filterwarnings("ignore")
import time
from features import tool_get_event, system_prompt_get_event
from services.llm.llm_config import LLM
from utils import *
# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")
weekdays = get_weekdays_context()

@pytest.fixture(scope="module")
def llm_extraction():
    return LLM(
        system_message=system_prompt_get_event,
        tool=tool_get_event,
        temperature=0.1
    )

@pytest.mark.parametrize("prompt, start_date, end_date, expected_query_type",[
    # Truy vấn lịch trong ngày cụ thể
    ("Lịch của tôi ngày mai có những gì?", tomorrow, tomorrow, "events"),
    ("Tôi có sự kiện nào vào ngày 15 tháng 6 không?", today.replace(day=15, month=6), today.replace(day=15, month=6), "events"),
    ("Kiểm tra lịch của tôi vào thứ Hai tuần này.", weekdays[0], weekdays[0], "events"),
    
    # Truy vấn lịch trong khoảng thời gian
    ("Lịch của tôi trong tuần này có những gì?", weekdays[0], weekdays[6], "events"),
    ("Tôi có những sự kiện nào trong tuần tới?", weekdays[7], weekdays[13], "events"),
    ("Hiển thị lịch của tôi từ ngày 10 đến ngày 15 tháng 6.", today.replace(day=10, month=6), today.replace(day=15, month=6), "events"),
    
    # Truy vấn lịch vào buổi cụ thể
    ("Lịch buổi sáng ngày mai của tôi có gì không?", tomorrow, tomorrow, "events_morning"),
    ("Tôi có sự kiện nào vào buổi chiều thứ Hai không?", weekdays[0], weekdays[0], "events_afternoon"),
    ("Kiểm tra lịch buổi tối ngày 20 tháng 6 của tôi.", today.replace(day=20, month=6), today.replace(day=20, month=6), "events_evening"),
    
    # Truy vấn lịch cho sự kiện cụ thể
    ("Tôi có lịch họp nào vào ngày mai không?", tomorrow, tomorrow, "events_meeting"),
    ("Kiểm tra xem tôi có lịch khám bệnh nào trong tuần này không?", weekdays[0], weekdays[6], "events_medical"),
    ("Tôi có hẹn gặp khách hàng nào vào thứ Sáu tuần này không?", weekdays[4], weekdays[4], "events_client"),
    
    # Truy vấn phức tạp
    ("Tôi có lịch họp nào vào buổi sáng ngày mai không?", tomorrow, tomorrow, "events_meeting_morning"),
    ("Kiểm tra xem tôi có lịch tập gym vào buổi chiều trong tuần này không?", weekdays[0], weekdays[6], "events_gym_afternoon"),
    ("Có sự kiện gia đình nào vào cuối tuần này không?", weekdays[5], weekdays[6], "events_family"),
    
    # Truy vấn lịch ở địa điểm cụ thể
    ("Tôi có lịch nào tại văn phòng vào ngày mai không?", tomorrow, tomorrow, "events_location"),
    ("Kiểm tra xem tôi có sự kiện nào tại nhà hàng trong tuần này không?", weekdays[0], weekdays[6], "events_location"),
    ("Tôi có hẹn nào tại bệnh viện Bạch Mai trong tháng này không?", today.replace(day=1), today.replace(day=today.day), "events_location"),
],)

def test_get_multi_calendar(llm_extraction, prompt, start_date, end_date, expected_query_type):
    result = llm_extraction(prompt)
    datetime_ranges = result["datetime_ranges"][0]
    
    start_datetime = start_date.strftime("%Y-%m-%d")
    end_datetime = end_date.strftime("%Y-%m-%d")
    
    today_str = today.strftime("%Y-%m-%d")
    start_assertion = start_datetime in datetime_ranges["start_datetime"]
    end_assertion = end_datetime in datetime_ranges["end_datetime"]
    query_type_assertion = expected_query_type in datetime_ranges.get("query_type", "events")
    
    error_file = f"log/get_multi_calendar_{today_str}.txt"
    if not start_assertion or not end_assertion or not query_type_assertion:
        with open(error_file, "a", encoding="utf-8") as f:
            if not start_assertion:
                f.write(f"Start date mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{start_datetime}'\n")
                f.write(f"  GenAI: '{datetime_ranges['start_datetime']}'\n\n")
            if not end_assertion:
                f.write(f"End date mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{end_datetime}'\n")
                f.write(f"  GenAI: '{datetime_ranges['end_datetime']}'\n\n")
            if not query_type_assertion:
                f.write(f"Query type mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_query_type}'\n")
                f.write(f"  GenAI: '{datetime_ranges.get('query_type', 'events')}'\n\n")
    
    assert start_assertion, f"Failed for input '{prompt}'. Mong muốn '{start_datetime}' in GenAI '{datetime_ranges['start_datetime']}'"
    assert end_assertion, f"Failed for input '{prompt}'. Mong muốn '{end_datetime}' in GenAI '{datetime_ranges['end_datetime']}'"
    assert query_type_assertion, f"Failed for input '{prompt}'. Mong muốn '{expected_query_type}' in GenAI '{datetime_ranges.get('query_type', 'events')}'"
    time.sleep(4)

if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/calendar/get_multi_calendar.py"])
