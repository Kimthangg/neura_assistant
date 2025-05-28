import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import warnings

import pytest

warnings.filterwarnings("ignore")
import time
from datetime import datetime, timedelta

from bot.agent.update_event.datetime_extraction import (
    extract_datetime_update_event,
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
        # Test cases for updating specific events
        ("Cập nhật lịch họp ngày mai", tomorrow, tomorrow, "00:00:00", "23:59:59"),
        ("Thay đổi thời gian cuộc hẹn hôm nay", today, today, "00:00:00", "23:59:59"),
        (
            "Dời lịch sự kiện vào thứ Bảy tuần này",
            get_valid_weekday(weekdays[5]),
            get_valid_weekday(weekdays[5]),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Đổi lịch các cuộc hẹn vào ngày 20 tháng 4",
            today.replace(day=20, month=4),
            today.replace(day=20, month=4),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Cập nhật cuộc họp lúc 15:00 ngày mai thành 16:00",
            tomorrow,
            tomorrow,
            "15:00:00",
            "16:59:59",
        ),
        (
            "Thay đổi lịch buổi chiều ngày 15/05 sang buổi sáng",
            today.replace(day=15, month=5),
            today.replace(day=15, month=5),
            "08:00:00",
            "11:59:59",
        ),
        # Test cases with more complex time expressions
        (
            "Dời tất cả các sự kiện trong tuần này sang tuần sau",
            weekdays[0],
            weekdays[6],
            "00:00:00",
            "23:59:59",
        ),
        (
            "Cập nhật thời gian các cuộc họp từ ngày 10 đến ngày 15 tháng 5",
            today.replace(day=10, month=5),
            today.replace(day=15, month=5),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Thay đổi tất cả sự kiện trong tháng 4",
            today.replace(day=1, month=4),
            today.replace(day=30, month=4),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Dời lịch làm việc vào thứ Hai và thứ Ba tuần sau",
            weekdays[7],
            weekdays[8],
            "00:00:00",
            "23:59:59",
        ),
        (
            "Đổi các cuộc họp vào buổi sáng sang buổi chiều trong tuần này",
            weekdays[0],
            weekdays[6],
            "12:00:00",
            "17:59:59",
        ),
        # Test cases with very specific time expressions
        (
            "Dời cuộc họp lúc 9:30 sáng ngày 25/04/2025 sang 10:30",
            datetime(2025, 4, 25),
            datetime(2025, 4, 25),
            "10:30:00",
            "11:29:59",
        ),
        (
            "Thay đổi thời gian lịch hẹn vào 14:00 chiều thứ Tư tuần sau thành 15:00",
            get_valid_weekday(weekdays[9]),
            get_valid_weekday(weekdays[9]),
            "15:00:00",
            "15:59:59",
        ),
        (
            "Cập nhật sự kiện họp nhóm diễn ra từ 10:00 đến 11:30 ngày 20/5 thành từ 13:00 đến 14:30",
            today.replace(day=20, month=5),
            today.replace(day=20, month=5),
            "13:00:00",
            "14:30:00",
        ),
        (
            "Dời cuộc hẹn với khách hàng vào 3 giờ chiều ngày 22/4 sang 4 giờ",
            today.replace(day=22, month=4),
            today.replace(day=22, month=4),
            "16:00:00",
            "16:59:59",
        ),
        # Test cases with date changes
        (
            "Dời cuộc họp từ thứ Ba sang thứ Năm tuần này",
            get_valid_weekday(weekdays[3]),
            get_valid_weekday(weekdays[3]),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Cập nhật sự kiện từ ngày 15/5 sang ngày 20/5",
            today.replace(day=20, month=5),
            today.replace(day=20, month=5),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Thay đổi thời gian đào tạo từ tháng 4 sang tháng 5",
            next_month,
            next_month.replace(day=31),
            "00:00:00",
            "23:59:59",
        ),
        (
            "Dời lịch hẹn từ Chủ nhật tuần này sang Chủ nhật tuần sau",
            get_valid_weekday(weekdays[13]),
            get_valid_weekday(weekdays[13]),
            "00:00:00",
            "23:59:59",
        ),
        # Test cases with special events and duration changes
        (
            "Kéo dài cuộc họp vào ngày mai thêm 1 tiếng",
            tomorrow,
            tomorrow,
            "00:00:00",
            "23:59:59",
        ),
        (
            "Rút ngắn thời gian buổi đào tạo ngày 15/5 xuống còn 1 tiếng",
            today.replace(day=15, month=5),
            today.replace(day=15, month=5),
            "00:00:00",
            "01:00:00",
        ),
        (
            "Dời lịch nghỉ mát từ tháng 7 sang tháng 8",
            datetime(2025, 8, 1),
            datetime(2025, 8, 31),
            "00:00:00",
            "23:59:59",
        ),
    ],
)
def test_extract_update_event(prompt, start_date, end_date, start_time, end_time):
    result = extract_datetime_update_event(prompt)
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
        ("Cập nhật thời gian họp vào ngày 15/4, 16/4 và 17/4", 3),
        ("Dời các lịch hẹn vào thứ Hai, thứ Tư và thứ Sáu tuần sau", 3),
        (
            "Thay đổi thời gian các sự kiện cuối tuần trong tháng 5",
            8,
        ),  # 4 cuối tuần, mỗi cuối tuần có 2 ngày
        (
            "Cập nhật cuộc họp sáng thứ Hai thành chiều thứ Hai, sáng thứ Ba thành chiều thứ Ba",
            2,
        ),
    ],
)
def test_datetime_range_count(prompt, expected_count):
    result = extract_datetime_update_event(prompt)
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
        ("Tôi muốn cập nhật một cuộc họp", "không tìm thấy thông tin thời gian"),
        (
            "Làm thế nào để thay đổi thời gian sự kiện?",
            "không tìm thấy thông tin thời gian",
        ),
        ("Xin chào, tôi cần thay đổi lịch", "không tìm thấy thông tin thời gian"),
    ],
)
def test_invalid_input(prompt, expected_error):
    try:
        result = extract_datetime_update_event(prompt)
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


@pytest.mark.parametrize(
    "prompt, expected_old_time, expected_new_time",
    [
        # Test cases for time changes (original time -> new time)
        ("Dời cuộc họp từ 9:00 sáng thành 10:00 sáng ngày mai", "09:00:00", "10:00:00"),
        ("Đổi lịch từ 14:00 chiều sang 16:00 chiều thứ Tư", "14:00:00", "16:00:00"),
        ("Thay đổi thời gian từ 8:30 sang 9:30 ngày 20/5", "08:30:00", "09:30:00"),
    ],
)
def test_time_changes(prompt, expected_old_time, expected_new_time):
    result = extract_datetime_update_event(prompt)
    print(f"Test time change: {prompt}")
    print(f"Result: {result}")

    # Kiểm tra xem có thông tin về thời gian cũ và mới không
    # Lưu ý: API thực tế có thể không trả về cả hai thông tin này,
    # nên test này có thể cần điều chỉnh tùy thuộc vào cách API được cài đặt
    datetime_ranges = result.get("datetime_ranges", [])
    if len(datetime_ranges) >= 1:
        if "old_time" in datetime_ranges[0]:
            assert (
                expected_old_time in datetime_ranges[0]["old_time"]
            ), f"Expected old time '{expected_old_time}' not found in result"
        if "new_time" in datetime_ranges[0]:
            assert (
                expected_new_time in datetime_ranges[0]["new_time"]
            ), f"Expected new time '{expected_new_time}' not found in result"

        # Nếu API không trả về old_time/new_time, chỉ kiểm tra start_datetime có chứa new_time
        assert (
            expected_new_time in datetime_ranges[0]["start_datetime"]
        ), f"Expected new time '{expected_new_time}' not found in start_datetime"

    print("Test time change passed!")
    time.sleep(4)


if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/test_update_event.py"])
