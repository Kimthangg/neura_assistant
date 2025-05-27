import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import warnings

import pytest

warnings.filterwarnings("ignore")
import time
from datetime import datetime, timedelta

from bot.agent_calendar.delete_event.datetime_extraction import (
    extract_datetime_delete_event,
)
from utils import *

# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")
weekdays = get_weekdays_context()
next_month = today.replace(day=1) + timedelta(days=32)
next_month = next_month.replace(day=1)
next_year = today.replace(year=today.year + 1, month=1, day=1)


@pytest.mark.parametrize(
    "prompt, start_date, end_date, start_time, end_time",
    [
        # Test cases for deleting specific events
        ("Xóa lịch họp ngày mai", tomorrow, tomorrow, "00:00:00", "23:59:59"),
        ("Hủy cuộc hẹn hôm nay", today, today, "00:00:00", "23:59:59"),
        (
            "Xóa sự kiện vào thứ Bảy tuần này",
            get_valid_weekday(weekdays[5]),
            get_valid_weekday(weekdays[5]),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Hủy tất cả các cuộc hẹn vào ngày 20 tháng 4",
            today.replace(day=20, month=4),
            today.replace(day=20, month=4),
            "00:00:00",
            "23:59:59",
        ),
        ("Xóa cuộc họp lúc 15:00 ngày mai", tomorrow, tomorrow, "15:00:00", "15:59:59"),
        (
            "Hủy lịch buổi chiều ngày 15/05",
            today.replace(day=15, month=5),
            today.replace(day=15, month=5),
            "12:00:00",
            "17:59:59",
        ),
        # Test cases with more complex time expressions
        (
            "Xóa tất cả các sự kiện trong tuần này",
            weekdays[0],
            weekdays[6],
            "00:00:00",
            "23:59:59",
        ),
        (
            "Hủy các cuộc họp từ ngày 10 đến ngày 15 tháng 5",
            today.replace(day=10, month=5),
            today.replace(day=15, month=5),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xóa hết sự kiện trong tháng 4",
            today.replace(day=1, month=4),
            today.replace(day=30, month=4),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Hủy lịch làm việc vào thứ Hai và thứ Ba tuần sau",
            weekdays[7],
            weekdays[8],
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xóa các cuộc họp vào buổi sáng trong tuần này",
            weekdays[0],
            weekdays[6],
            "08:00:00",
            "11:59:59",
        ),
        # Test cases with very specific time expressions
        (
            "Xóa cuộc họp lúc 9:30 sáng ngày 25/04/2025",
            datetime(2025, 4, 25),
            datetime(2025, 4, 25),
            "09:30:00",
            "10:29:59",
        ),
        (
            "Hủy lịch hẹn vào 14:00 chiều thứ Tư tuần sau",
            get_valid_weekday(weekdays[9]),
            get_valid_weekday(weekdays[9]),
            "14:00:00",
            "14:59:59",
        ),
        (
            "Xóa sự kiện họp nhóm diễn ra từ 10:00 đến 11:30 ngày 20/5",
            today.replace(day=20, month=5),
            today.replace(day=20, month=5),
            "10:00:00",
            "11:30:00",
        ),
        (
            "Hủy cuộc hẹn với khách hàng vào 3 giờ chiều ngày 22/4",
            today.replace(day=22, month=4),
            today.replace(day=22, month=4),
            "15:00:00",
            "15:59:59",
        ),
        # Test cases with special events and holidays
        (
            "Xóa tất cả sự kiện vào dịp lễ 30/4 - 1/5",
            datetime(2025, 4, 30),
            datetime(2025, 5, 1),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Hủy các cuộc họp trong kỳ nghỉ Tết năm 2026",
            datetime(2026, 1, 20),
            datetime(2026, 2, 5),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xóa tất cả sự kiện vào ngày cuối năm",
            datetime(2025, 12, 31),
            datetime(2025, 12, 31),
            "00:00:00",
            "23:59:59",
        ),
    ],
)
def test_extract_delete_event(prompt, start_date, end_date, start_time, end_time):
    result = extract_datetime_delete_event(prompt)
    datetime_ranges = result["datetime_ranges"][0]

    start_datetime = start_date.strftime("%Y-%m-%d") + " " + start_time
    end_datetime = end_date.strftime("%Y-%m-%d") + " " + end_time
    print(f"Test: {prompt}")
    print(f"Expected: {start_datetime} - {end_datetime}")
    print(
        f"Actual: {datetime_ranges['start_datetime']} - {datetime_ranges['end_datetime']}"
    )
    assert (
        datetime_ranges["start_datetime"] == start_datetime
    ), f"Failed for input '{prompt}'. Expected '{start_datetime}' but got '{datetime_ranges['start_datetime']}'"
    assert (
        datetime_ranges["end_datetime"] == end_datetime
    ), f"Failed for input '{prompt}'. Expected '{end_datetime}' but got '{datetime_ranges['end_datetime']}'"
    print("Test passed!")
    time.sleep(4)


@pytest.mark.parametrize(
    "prompt, expected_count",
    [
        # Test số lượng khoảng thời gian trả về
        ("Xóa các cuộc họp vào ngày 15/4, 16/4 và 17/4", 3),
        ("Hủy tất cả lịch hẹn vào thứ Hai, thứ Tư và thứ Sáu tuần sau", 3),
        (
            "Xóa sự kiện trong các ngày cuối tuần của tháng 5",
            8,
        ),  # 4 cuối tuần, mỗi cuối tuần có 2 ngày
    ],
)
def test_datetime_range_count(prompt, expected_count):
    result = extract_datetime_delete_event(prompt)
    actual_count = len(result["datetime_ranges"])
    print(f"Test count: {prompt}")
    print(f"Expected count: {expected_count}, Actual count: {actual_count}")
    assert (
        actual_count == expected_count
    ), f"Failed for input '{prompt}'. Expected {expected_count} datetime ranges but got {actual_count}"
    print("Test count passed!")
    time.sleep(4)


@pytest.mark.parametrize(
    "prompt, expected_error",
    [
        # Test các trường hợp đầu vào không hợp lệ
        ("Tôi muốn xóa một cuộc họp", "không tìm thấy thông tin thời gian"),
        ("Làm thế nào để hủy một sự kiện?", "không tìm thấy thông tin thời gian"),
        ("Xin chào, tôi cần hủy lịch", "không tìm thấy thông tin thời gian"),
    ],
)
def test_invalid_input(prompt, expected_error):
    try:
        result = extract_datetime_delete_event(prompt)
        # Nếu không có exception, kiểm tra xem kết quả có chứa thông báo lỗi không
        print(f"Test invalid input: {prompt}")
        print(f"Result: {result}")
        if "error" in result:
            assert (
                expected_error.lower() in result["error"].lower()
            ), f"Error message doesn't match for input '{prompt}'"
        else:
            datetime_ranges = result.get("datetime_ranges", [])
            if not datetime_ranges:
                # Nếu không có datetime_ranges, xem như test pass
                print("No datetime ranges returned, test passed")
            else:
                # Nếu có datetime_ranges, kiểm tra xem nó có hợp lệ không
                start_datetime = datetime_ranges[0].get("start_datetime", "")
                end_datetime = datetime_ranges[0].get("end_datetime", "")
                if not start_datetime or not end_datetime:
                    print("Empty datetime range, test passed")
                else:
                    assert (
                        False
                    ), f"Expected error for input '{prompt}' but got valid datetime range"
    except Exception as e:
        # Nếu có exception, kiểm tra xem nó có chứa thông báo lỗi không
        assert (
            expected_error.lower() in str(e).lower()
        ), f"Unexpected exception for input '{prompt}': {str(e)}"
    print("Test invalid input passed!")
    time.sleep(4)


if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/test_delete_event.py"])
