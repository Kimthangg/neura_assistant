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

@pytest.mark.parametrize("prompt, start_date, end_date, expected_timeframe",[
    # Truy vấn thời gian trống trong ngày cụ thể
    ("Tôi có thời gian rảnh nào vào ngày mai?", tomorrow, tomorrow, "all_day"),
    ("Khi nào tôi rảnh vào thứ Hai tuần này?", weekdays[0], weekdays[0], "all_day"),
    ("Tìm thời gian trống cho tôi vào ngày 15 tháng 6.", today.replace(day=15, month=6), today.replace(day=15, month=6), "all_day"),
    
    # Truy vấn thời gian trống trong khoảng thời gian
    ("Tôi có thời gian rảnh nào trong tuần này?", weekdays[0], weekdays[6], "all_day"),
    ("Khi nào tôi rảnh trong tuần tới?", weekdays[7], weekdays[13], "all_day"),
    ("Tìm thời gian trống từ ngày 10 đến ngày 15 tháng 6.", today.replace(day=10, month=6), today.replace(day=15, month=6), "all_day"),
    
    # Truy vấn thời gian trống vào buổi cụ thể
    ("Tôi có thời gian rảnh buổi sáng ngày mai không?", tomorrow, tomorrow, "morning"),
    ("Khi nào tôi rảnh vào buổi chiều thứ Hai?", weekdays[0], weekdays[0], "afternoon"),
    ("Tôi có thời gian trống vào buổi tối ngày 20 tháng 6 không?", today.replace(day=20, month=6), today.replace(day=20, month=6), "evening"),
    
    # Truy vấn thời gian trống cho hoạt động cụ thể
    ("Tìm thời gian trống để họp nhóm vào ngày mai.", tomorrow, tomorrow, "all_day"),
    ("Khi nào tôi có thể đặt lịch khám răng trong tuần này?", weekdays[0], weekdays[6], "all_day"),
    ("Tôi có thời gian rảnh để đi ăn tối với bạn vào thứ Sáu tuần này không?", weekdays[4], weekdays[4], "evening"),
    
    # Truy vấn phức tạp
    ("Tôi cần tìm thời gian trống để họp nhóm vào buổi sáng ngày mai.", tomorrow, tomorrow, "morning"),
    ("Khi nào tôi có thể đặt lịch tập gym vào buổi chiều trong tuần này?", weekdays[0], weekdays[6], "afternoon"),
    ("Tìm thời gian trống để đi ăn tối với gia đình vào buổi tối cuối tuần này.", weekdays[5], weekdays[6], "evening"),
],)

def test_get_freetime(llm_extraction, prompt, start_date, end_date, expected_timeframe):
    result = llm_extraction(prompt)
    datetime_ranges = result["datetime_ranges"][0]
    
    start_datetime = start_date.strftime("%Y-%m-%d")
    end_datetime = end_date.strftime("%Y-%m-%d")
    
    today_str = today.strftime("%Y-%m-%d")
    start_assertion = start_datetime in datetime_ranges["start_datetime"]
    end_assertion = end_datetime in datetime_ranges["end_datetime"]
    timeframe_assertion = expected_timeframe in datetime_ranges.get("timeframe", "all_day")
    
    error_file = f"log/get_freetime_{today_str}.txt"
    if not start_assertion or not end_assertion or not timeframe_assertion:
        with open(error_file, "a", encoding="utf-8") as f:
            if not start_assertion:
                f.write(f"Start date mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{start_datetime}'\n")
                f.write(f"  GenAI: '{datetime_ranges['start_datetime']}'\n\n")
            if not end_assertion:
                f.write(f"End date mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{end_datetime}'\n")
                f.write(f"  GenAI: '{datetime_ranges['end_datetime']}'\n\n")
            if not timeframe_assertion:
                f.write(f"Timeframe mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_timeframe}'\n")
                f.write(f"  GenAI: '{datetime_ranges.get('timeframe', 'all_day')}'\n\n")
    
    assert start_assertion, f"Failed for input '{prompt}'. Mong muốn '{start_datetime}' in GenAI '{datetime_ranges['start_datetime']}'"
    assert end_assertion, f"Failed for input '{prompt}'. Mong muốn '{end_datetime}' in GenAI '{datetime_ranges['end_datetime']}'"
    assert timeframe_assertion, f"Failed for input '{prompt}'. Mong muốn '{expected_timeframe}' in GenAI '{datetime_ranges.get('timeframe', 'all_day')}'"
    time.sleep(4)

if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/calendar/get_freetime.py"])
