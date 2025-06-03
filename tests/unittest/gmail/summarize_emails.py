import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import warnings
import pytest
warnings.filterwarnings("ignore")
import time
from features import tool_summarize_emails, system_prompt_summarize_emails
from services.llm.llm_config import LLM
from utils import *
# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")
weekdays = get_weekdays_context()

@pytest.fixture(scope="module")
def llm_extraction():
    return LLM(
        system_message=system_prompt_summarize_emails,
        tool=tool_summarize_emails,
        temperature=0.1
    )

@pytest.mark.parametrize("prompt, expected_sender, expected_time_range, expected_categories",[
    # Tóm tắt email từ người gửi cụ thể
    ("Tóm tắt email từ nguyenvana@gmail.com.", "nguyenvana@gmail.com", "all", ["all"]),
    ("Tổng hợp thư từ công ty ABC.", "công ty ABC", "all", ["all"]),
    ("Tóm tắt email của Nguyễn Văn A.", "Nguyễn Văn A", "all", ["all"]),
    
    # Tóm tắt email trong khoảng thời gian
    ("Tóm tắt email nhận được hôm nay.", "all", "today", ["all"]),
    ("Tổng hợp thư trong tuần này.", "all", "this_week", ["all"]),
    ("Tóm tắt email nhận được trong tháng trước.", "all", "last_month", ["all"]),
    
    # Tóm tắt email từ người gửi trong khoảng thời gian
    ("Tóm tắt email từ nguyenvana@gmail.com trong hôm nay.", "nguyenvana@gmail.com", "today", ["all"]),
    ("Tổng hợp thư từ công ty ABC trong tuần này.", "công ty ABC", "this_week", ["all"]),
    ("Tóm tắt email của Nguyễn Văn A trong tháng qua.", "Nguyễn Văn A", "last_month", ["all"]),
    
    # Tóm tắt email theo danh mục
    ("Tóm tắt email công việc.", "all", "all", ["work"]),
    ("Tổng hợp thư liên quan đến dự án X.", "all", "all", ["project"]),
    ("Tóm tắt email về họp nhóm.", "all", "all", ["meeting"]),
    
    # Tóm tắt email theo danh mục từ người gửi
    ("Tóm tắt email công việc từ sếp.", "sếp", "all", ["work"]),
    ("Tổng hợp thư về dự án X từ PM.", "PM", "all", ["project"]),
    ("Tóm tắt email về họp từ phòng nhân sự.", "phòng nhân sự", "all", ["meeting"]),
    
    # Tóm tắt email theo danh mục trong khoảng thời gian
    ("Tóm tắt email công việc trong tuần này.", "all", "this_week", ["work"]),
    ("Tổng hợp thư về dự án X trong tháng qua.", "all", "last_month", ["project"]),
    ("Tóm tắt email về họp trong hôm nay.", "all", "today", ["meeting"]),
    
    # Tóm tắt email phức tạp
    ("Tóm tắt email công việc từ sếp trong tuần này.", "sếp", "this_week", ["work"]),
    ("Tổng hợp thư về dự án X từ PM trong tháng qua.", "PM", "last_month", ["project"]),
    ("Tóm tắt email quan trọng nhận được hôm nay.", "all", "today", ["important"]),
],)

def test_summarize_emails(llm_extraction, prompt, expected_sender, expected_time_range, expected_categories):
    result = llm_extraction(prompt)
    email_summary = result["email_summary"]
    
    today_str = today.strftime("%Y-%m-%d")
    sender_assertion = expected_sender == "all" or expected_sender in email_summary.get("sender", "all")
    time_range_assertion = expected_time_range == "all" or expected_time_range in email_summary.get("time_range", "all")
    
    # Kiểm tra danh mục
    categories_match = False
    if expected_categories == ["all"]:
        categories_match = True
    else:
        for category in expected_categories:
            if category in email_summary.get("categories", []):
                categories_match = True
                break
    
    error_file = f"log/summarize_emails_{today_str}.txt"
    if not sender_assertion or not time_range_assertion or not categories_match:
        with open(error_file, "a", encoding="utf-8") as f:
            if not sender_assertion:
                f.write(f"Sender mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_sender}'\n")
                f.write(f"  GenAI: '{email_summary.get('sender', 'all')}'\n\n")
            if not time_range_assertion:
                f.write(f"Time range mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_time_range}'\n")
                f.write(f"  GenAI: '{email_summary.get('time_range', 'all')}'\n\n")
            if not categories_match:
                f.write(f"Categories mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_categories}'\n")
                f.write(f"  GenAI: '{email_summary.get('categories', [])}'\n\n")
    
    assert sender_assertion, f"Failed for input '{prompt}'. Mong muốn sender '{expected_sender}' in GenAI '{email_summary.get('sender', 'all')}'"
    assert time_range_assertion, f"Failed for input '{prompt}'. Mong muốn time range '{expected_time_range}' in GenAI '{email_summary.get('time_range', 'all')}'"
    assert categories_match, f"Failed for input '{prompt}'. Mong muốn categories '{expected_categories}' in GenAI '{email_summary.get('categories', [])}'"
    time.sleep(4)

if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/gmail/summarize_emails.py"])
