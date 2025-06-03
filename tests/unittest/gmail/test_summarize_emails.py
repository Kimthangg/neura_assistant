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

@pytest.mark.parametrize("prompt, expected_sender, expected_subject, expected_keyword, expected_start_date, expected_end_date, expected_incorrect_datetime",[
    # Tóm tắt email từ người gửi cụ thể
    ("Tóm tắt email từ nguyenvana@gmail.com.", "nguyenvana@gmail.com", "", "", "", "", False),
    ("Tổng hợp thư từ công ty ABC.", "công ty ABC", "", "", "", "", False),
    ("Tóm tắt email của Nguyễn Văn A.", "Nguyễn Văn A", "", "", "", "", False),
    
    # Tóm tắt email trong khoảng thời gian
    ("Tóm tắt email nhận được hôm nay.", "", "", "", today.strftime("%Y-%m-%d"), tomorrow.strftime("%Y-%m-%d"), False),
    ("Tổng hợp thư trong tuần này.", "", "", "", "", "", False),
    ("Tóm tắt email nhận được trong tháng trước.", "", "", "", "", "", False),
    
    # Tóm tắt email từ người gửi trong khoảng thời gian
    ("Tóm tắt email từ nguyenvana@gmail.com trong hôm nay.", "nguyenvana@gmail.com", "", "", today.strftime("%Y-%m-%d"), tomorrow.strftime("%Y-%m-%d"), False),
    ("Tổng hợp thư từ công ty ABC trong tuần này.", "công ty ABC", "", "", "", "", False),
    ("Tóm tắt email của Nguyễn Văn A trong tháng qua.", "Nguyễn Văn A", "", "", "", "", False),
    
    # Tóm tắt email theo chủ đề
    ("Tóm tắt email về báo cáo công việc.", "", "báo cáo công việc", "", "", "", False),
    ("Tổng hợp thư liên quan đến dự án X.", "", "dự án X", "", "", "", False),
    ("Tóm tắt email về họp nhóm.", "", "họp nhóm", "", "", "", False),
    
    # Tóm tắt email với từ khóa
    ("Tóm tắt email có chứa từ khóa hợp đồng.", "", "", "hợp đồng", "", "", False),
    ("Tổng hợp thư có từ khóa báo cáo tài chính.", "", "", "báo cáo tài chính", "", "", False),
    ("Tóm tắt email chứa thông tin dự án.", "", "", "thông tin dự án", "", "", False),
    
    # Tóm tắt email phức tạp
    ("Tóm tắt email từ sếp về báo cáo hôm nay.", "sếp", "báo cáo", "", today.strftime("%Y-%m-%d"), tomorrow.strftime("%Y-%m-%d"), False),
    ("Tổng hợp thư từ PM về dự án X có chứa từ khóa deadline.", "PM", "dự án X", "deadline", "", "", False),
    ("Tóm tắt email từ HR về cuộc họp tuần này.", "HR", "cuộc họp", "", "", "", False),
    
    # Test trường hợp ngày không hợp lệ
    ("Tóm tắt email ngày 30/2.", "", "", "", "", "", True),
    ("Tóm tắt email ngày 31/4.", "", "", "", "", "", True),
    ("Tóm tắt email ngày 32/1.", "", "", "", "", "", True),
],)

def test_summarize_emails(llm_extraction, prompt, expected_sender, expected_subject, expected_keyword, expected_start_date, expected_end_date, expected_incorrect_datetime):
    result = llm_extraction(prompt)
    email_data = result["extract_datetime"]
    
    today_str = today.strftime("%Y-%m-%d")
    
    # Kiểm tra sender
    sender_match = True
    if expected_sender:
        sender_match = expected_sender in email_data.get("sender", "")
    
    # Kiểm tra subject
    subject_match = True
    if expected_subject:
        subject_match = expected_subject in email_data.get("subject", "")
    
    # Kiểm tra keyword
    keyword_match = True
    if expected_keyword:
        keyword_match = expected_keyword in email_data.get("keyword", "")
    
    # Kiểm tra start_date
    start_date_match = True
    if expected_start_date:
        start_date_match = expected_start_date == email_data.get("start_date", "")
    
    # Kiểm tra end_date
    end_date_match = True
    if expected_end_date:
        end_date_match = expected_end_date == email_data.get("end_date", "")
    
    # Kiểm tra incorrect_datetime
    incorrect_datetime_match = expected_incorrect_datetime == email_data.get("incorrect_datetime", False)
    
    error_file = f"log/summarize_emails_{today_str}.txt"
    if not all([sender_match, subject_match, keyword_match, start_date_match, end_date_match, incorrect_datetime_match]):
        with open(error_file, "a", encoding="utf-8") as f:
            if not sender_match:
                f.write(f"Sender mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_sender}'\n")
                f.write(f"  GenAI: '{email_data.get('sender', '')}'\n\n")
            if not subject_match:
                f.write(f"Subject mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_subject}'\n")
                f.write(f"  GenAI: '{email_data.get('subject', '')}'\n\n")
            if not keyword_match:
                f.write(f"Keyword mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_keyword}'\n")
                f.write(f"  GenAI: '{email_data.get('keyword', '')}'\n\n")
            if not start_date_match:
                f.write(f"Start date mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_start_date}'\n")
                f.write(f"  GenAI: '{email_data.get('start_date', '')}'\n\n")
            if not end_date_match:
                f.write(f"End date mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_end_date}'\n")
                f.write(f"  GenAI: '{email_data.get('end_date', '')}'\n\n")
            if not incorrect_datetime_match:
                f.write(f"Incorrect datetime mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{expected_incorrect_datetime}'\n")
                f.write(f"  GenAI: '{email_data.get('incorrect_datetime', False)}'\n\n")
    
    assert sender_match, f"Failed for input '{prompt}'. Mong muốn sender chứa '{expected_sender}' nhưng GenAI trả về '{email_data.get('sender', '')}'"
    assert subject_match, f"Failed for input '{prompt}'. Mong muốn subject chứa '{expected_subject}' nhưng GenAI trả về '{email_data.get('subject', '')}'"
    assert keyword_match, f"Failed for input '{prompt}'. Mong muốn keyword chứa '{expected_keyword}' nhưng GenAI trả về '{email_data.get('keyword', '')}'"
    assert start_date_match, f"Failed for input '{prompt}'. Mong muốn start_date '{expected_start_date}' nhưng GenAI trả về '{email_data.get('start_date', '')}'"
    assert end_date_match, f"Failed for input '{prompt}'. Mong muốn end_date '{expected_end_date}' nhưng GenAI trả về '{email_data.get('end_date', '')}'"
    assert incorrect_datetime_match, f"Failed for input '{prompt}'. Mong muốn incorrect_datetime '{expected_incorrect_datetime}' nhưng GenAI trả về '{email_data.get('incorrect_datetime', False)}'"
    time.sleep(4)

if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/gmail/test_summarize_emails.py"])
