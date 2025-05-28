import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import warnings

import pytest

warnings.filterwarnings("ignore")
import time
from datetime import datetime, timedelta

from bot.agent.get_event.datetime_extraction import extract_datetime_get_event
from utils import *

# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")
weekdays = get_weekdays_context()
next_month = today.replace(day=1) + timedelta(days=32)
next_month = next_month.replace(day=1)
next_year = today.replace(year=today.year + 1, month=1, day=1)


@pytest.mark.parametrize(
    "prompt, intent, start_date, end_date, start_time, end_time",
    [
        # Test cases for get_first_calendar
        (
            "Xem lịch họp ngày mai",
            "get_first_calendar",
            tomorrow,
            tomorrow,
            "00:00:00",
            "23:59:59",
        ),
        (
            "Kiểm tra lịch hôm nay của tôi",
            "get_first_calendar",
            today,
            today,
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xem lịch sự kiện vào thứ Bảy tuần này",
            "get_first_calendar",
            get_valid_weekday(weekdays[5]),
            get_valid_weekday(weekdays[5]),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Nhắc tôi về các cuộc hẹn vào ngày 20 tháng 4",
            "get_first_calendar",
            today.replace(day=20, month=4),
            today.replace(day=20, month=4),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xem sự kiện lúc 15:00 ngày mai",
            "get_first_calendar",
            tomorrow,
            tomorrow,
            "15:00:00",
            "15:59:59",
        ),
        (
            "Xem lịch buổi chiều ngày 15/05",
            "get_first_calendar",
            today.replace(day=15, month=5),
            today.replace(day=15, month=5),
            "12:00:00",
            "17:59:59",
        ),
        # Thêm testcase mới cho get_first_calendar
        (
            "Hiển thị cuộc họp đầu tiên trong ngày 25/04/2025",
            "get_first_calendar",
            datetime(2025, 4, 25),
            datetime(2025, 4, 25),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Kiểm tra lịch họp vào thứ Tư tuần sau lúc 10 giờ sáng",
            "get_first_calendar",
            get_valid_weekday(weekdays[9]),
            get_valid_weekday(weekdays[9]),
            "10:00:00",
            "10:59:59",
        ),
        (
            "Xem cuộc hẹn đầu tiên của cuối tháng 5",
            "get_first_calendar",
            datetime(2025, 5, 25),
            datetime(2025, 5, 31),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Hiển thị lịch buổi trưa Chủ nhật tuần tới",
            "get_first_calendar",
            get_valid_weekday(weekdays[13]),
            get_valid_weekday(weekdays[13]),
            "11:00:00",
            "13:59:59",
        ),
        (
            "Xem cuộc họp đầu tiên của tháng 6 năm nay",
            "get_first_calendar",
            datetime(2025, 6, 1),
            datetime(2025, 6, 1),
            "00:00:00",
            "23:59:59",
        ),
        # Test cases for get_freetime
        (
            "Tôi có thời gian rảnh nào vào ngày mai?",
            "get_freetime",
            tomorrow,
            tomorrow,
            "00:00:00",
            "23:59:59",
        ),
        (
            "Kiểm tra xem tôi có thể gặp khách hàng lúc nào trong tuần này",
            "get_freetime",
            weekdays[0],
            weekdays[6],
            "08:00:00",
            "17:00:00",
        ),
        (
            "Tôi rảnh lúc nào vào thứ Sáu?",
            "get_freetime",
            get_valid_weekday(weekdays[4]),
            get_valid_weekday(weekdays[4]),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Kiểm tra thời gian rảnh vào ngày 20/04 buổi sáng",
            "get_freetime",
            today.replace(day=20, month=4),
            today.replace(day=20, month=4),
            "08:00:00",
            "11:59:59",
        ),
        (
            "Tôi có thể sắp xếp cuộc họp vào lúc nào trong tuần tới?",
            "get_freetime",
            weekdays[7],
            weekdays[13],
            "08:00:00",
            "17:00:00",
        ),
        (
            "Kiểm tra khung giờ rảnh từ 12/04 đến 15/04",
            "get_freetime",
            today.replace(day=12, month=4),
            today.replace(day=15, month=4),
            "00:00:00",
            "23:59:59",
        ),
        # Thêm testcase mới cho get_freetime
        (
            "Tôi có thời gian trống nào trong 3 ngày tới không?",
            "get_freetime",
            today,
            today + timedelta(days=2),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Khi nào tôi rảnh trong tuần cuối tháng 5?",
            "get_freetime",
            datetime(2025, 5, 26),
            datetime(2025, 5, 31),
            "09:00:00",
            "17:00:00",
        ),
        (
            "Kiểm tra lịch trống vào buổi tối các ngày cuối tuần tháng này",
            "get_freetime",
            min(get_valid_weekday(weekdays[5]), get_valid_weekday(weekdays[12])),
            max(get_valid_weekday(weekdays[6]), get_valid_weekday(weekdays[13])),
            "18:00:00",
            "22:00:00",
        ),
        (
            "Tôi cần biết khung giờ rảnh để sắp xếp họp trong kỳ nghỉ lễ 30/4",
            "get_freetime",
            datetime(2025, 4, 30),
            datetime(2025, 5, 1),
            "08:00:00",
            "17:00:00",
        ),
        (
            "Tôi muốn đặt lịch khám bệnh, xem khi nào tôi rảnh trong 2 tuần tới",
            "get_freetime",
            today,
            today + timedelta(days=14),
            "08:00:00",
            "17:00:00",
        ),
        (
            "Xem lúc nào tôi có thể sắp xếp cuộc họp với khách hàng vào ngày 18/4 hoặc 19/4",
            "get_freetime",
            datetime(2025, 4, 18),
            datetime(2025, 4, 19),
            "09:00:00",
            "17:00:00",
        ),
        # Test cases for get_multi_calendar
        (
            "Xem tất cả các cuộc họp trong tuần này",
            "get_multi_calendar",
            weekdays[0],
            weekdays[6],
            "00:00:00",
            "23:59:59",
        ),
        (
            "Liệt kê các sự kiện từ ngày 10 đến ngày 15 tháng 5",
            "get_multi_calendar",
            today.replace(day=10, month=5),
            today.replace(day=15, month=5),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Tôi cần biết tất cả các sự kiện trong tháng 4",
            "get_multi_calendar",
            today.replace(day=1, month=4),
            today.replace(day=30, month=4),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xem lịch của tôi vào thứ Hai và thứ Ba tuần sau",
            "get_multi_calendar",
            weekdays[7],
            weekdays[8],
            "00:00:00",
            "23:59:59",
        ),
        (
            "Hiển thị các cuộc họp vào buổi sáng trong tuần này",
            "get_multi_calendar",
            weekdays[0],
            weekdays[6],
            "08:00:00",
            "11:59:59",
        ),
        (
            "Lấy tất cả lịch hẹn trong quý 2 năm nay",
            "get_multi_calendar",
            today.replace(day=1, month=4),
            today.replace(day=30, month=6),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Tôi cần xem tất cả các sự kiện vào thứ Bảy và Chủ Nhật trong tháng này",
            "get_multi_calendar",
            get_valid_weekday(weekdays[5]),
            get_valid_weekday(weekdays[13]),
            "00:00:00",
            "23:59:59",
        ),
        # Thêm testcase mới cho get_multi_calendar
        (
            "Hiển thị danh sách cuộc họp trong 10 ngày tới",
            "get_multi_calendar",
            today,
            today + timedelta(days=10),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Liệt kê tất cả các sự kiện trong tháng 5 và tháng 6",
            "get_multi_calendar",
            datetime(2025, 5, 1),
            datetime(2025, 6, 30),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xem các cuộc họp vào buổi chiều các ngày làm việc trong tuần này",
            "get_multi_calendar",
            weekdays[0],
            weekdays[4],
            "12:00:00",
            "17:59:59",
        ),
        (
            "Hiển thị các sự kiện trong dịp lễ 30/4 - 1/5",
            "get_multi_calendar",
            datetime(2025, 4, 30),
            datetime(2025, 5, 1),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Liệt kê các cuộc họp quan trọng trong nửa đầu năm 2025",
            "get_multi_calendar",
            datetime(2025, 1, 1),
            datetime(2025, 6, 30),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Xem tất cả các buổi đào tạo vào thứ Ba và thứ Năm trong tháng tới",
            "get_multi_calendar",
            next_month.replace(day=1),
            (
                next_month.replace(day=28)
                if next_month.month != 2
                else next_month.replace(day=28)
            ),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Hiển thị các cuộc hẹn với khách hàng trong quý 3 năm nay",
            "get_multi_calendar",
            datetime(2025, 7, 1),
            datetime(2025, 9, 30),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Lấy lịch làm việc từ Tết dương lịch đến Tết âm lịch năm 2026",
            "get_multi_calendar",
            datetime(2026, 1, 1),
            datetime(2026, 2, 15),
            "00:00:00",
            "23:59:59",
        ),
    ],
)
def test_extract_get_event(prompt, intent, start_date, end_date, start_time, end_time):
    result = extract_datetime_get_event(prompt, intent)
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
    ), f"Failed for input '{prompt}' with intent '{intent}'. Expected '{start_datetime}' but got '{datetime_ranges['start_datetime']}'"
    assert (
        datetime_ranges["end_datetime"] == end_datetime
    ), f"Failed for input '{prompt}' with intent '{intent}'. Expected '{end_datetime}' but got '{datetime_ranges['end_datetime']}'"
    print("Test passed!")
    time.sleep(4)


@pytest.mark.parametrize(
    "prompt, intent, expected_count",
    [
        # Test số lượng khoảng thời gian trả về
        ("Hiển thị lịch họp vào ngày 15/4, 16/4 và 17/4", "get_multi_calendar", 3),
        (
            "Tôi rảnh lúc nào vào thứ Hai, thứ Tư và thứ Sáu tuần sau?",
            "get_freetime",
            3,
        ),
        (
            "Kiểm tra lịch các ngày cuối tuần trong tháng 5",
            "get_multi_calendar",
            8,
        ),  # 4 cuối tuần, mỗi cuối tuần có 2 ngày
    ],
)
def test_datetime_range_count(prompt, intent, expected_count):
    result = extract_datetime_get_event(prompt, intent)
    actual_count = len(result["datetime_ranges"])
    print(f"Test count: {prompt}")
    print(f"Expected count: {expected_count}, Actual count: {actual_count}")
    assert (
        actual_count == expected_count
    ), f"Failed for input '{prompt}'. Expected {expected_count} datetime ranges but got {actual_count}"
    print("Test count passed!")
    time.sleep(4)


@pytest.mark.parametrize(
    "prompt, intent, expected_error",
    [
        # Test các trường hợp đầu vào không hợp lệ
        (
            "Hôm nay trời đẹp quá",
            "get_first_calendar",
            "không tìm thấy thông tin thời gian",
        ),
        ("Tôi muốn đặt lịch", "get_freetime", "không tìm thấy thông tin thời gian"),
        (
            "Xin chào, bạn có khỏe không?",
            "get_multi_calendar",
            "không tìm thấy thông tin thời gian",
        ),
    ],
)
def test_invalid_input(prompt, intent, expected_error):
    try:
        result = extract_datetime_get_event(prompt, intent)
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
    pytest.main(["-sv", "tests/unittest/test_get_event.py"])
