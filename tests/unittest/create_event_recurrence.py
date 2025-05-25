import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import warnings

import pytest

warnings.filterwarnings("ignore")
import time

from bot.agent_calendar.create_event.datetime_extraction import (
    extract_datetime_from_text,
)
from utils import *

# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")

weekdays = get_weekdays_context()


@pytest.mark.parametrize(
    "prompt, start_date, end_date, start_time, end_time, rrule",
    [
        # DAILY recurring events - Sự kiện lặp lại hàng ngày
        (
            "Tạo lịch tập thể dục hàng ngày vào lúc 6:00 sáng.",
            today,
            today,
            "06:00:00",
            "06:00:00",
            "RRULE:FREQ=DAILY",
        ),
        (
            "Đặt lịch họp triển khai dự án mỗi ngày lúc 9:00 sáng trong vòng 2 tuần.",
            today,
            today,
            "09:00:00",
            "09:00:00",
            "RRULE:FREQ=DAILY;COUNT=14",
        ),
        (
            "Tạo nhắc nhở uống thuốc hàng ngày vào 8 giờ sáng và 8 giờ tối.",
            today,
            today,
            "08:00:00",
            "08:00:00",
            "RRULE:FREQ=DAILY;BYHOUR=8,20",
        ),
        (
            "Đặt lịch cập nhật tiến độ công việc mỗi ngày vào 16:30.",
            today,
            today,
            "16:30:00",
            "16:30:00",
            "RRULE:FREQ=DAILY",
        ),
        (
            "Lên lịch nhắc uống nước mỗi 2 tiếng từ 8 giờ sáng đến 6 giờ chiều hàng ngày.",
            today,
            today,
            "08:00:00",
            "08:05:00",
            "RRULE:FREQ=DAILY;BYHOUR=8,10,12,14,16,18",
        ),
        # WEEKLY recurring events - Sự kiện lặp lại hàng tuần
        (
            "Tạo lịch họp nhóm mỗi thứ Hai vào lúc 10:00 sáng.",
            get_valid_weekday(weekdays[0]),
            get_valid_weekday(weekdays[0]),
            "10:00:00",
            "10:00:00",
            "RRULE:FREQ=WEEKLY;BYDAY=MO",
        ),
        (
            "Đặt lịch học tiếng Anh mỗi thứ Ba và thứ Năm lúc 19:30.",
            get_valid_weekday(weekdays[1]),
            get_valid_weekday(weekdays[1]),
            "19:30:00",
            "19:30:00",
            "RRULE:FREQ=WEEKLY;BYDAY=TU,TH",
        ),
        (
            "Lên lịch tập gym hàng tuần vào thứ Tư, thứ Sáu và Chủ Nhật lúc 18:00.",
            get_valid_weekday(weekdays[2]),
            get_valid_weekday(weekdays[2]),
            "18:00:00",
            "18:00:00",
            "RRULE:FREQ=WEEKLY;BYDAY=WE,FR,SU",
        ),
        (
            "Đặt lịch họp phòng marketing mỗi 2 tuần vào thứ Năm lúc 14:00.",
            get_valid_weekday(weekdays[3]),
            get_valid_weekday(weekdays[3]),
            "14:00:00",
            "14:00:00",
            "RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TH",
        ),
        (
            "Tạo lịch đi dạo buổi sáng hàng tuần vào thứ Bảy và Chủ Nhật lúc 6:30.",
            get_valid_weekday(weekdays[5]),
            get_valid_weekday(weekdays[5]),
            "06:30:00",
            "06:30:00",
            "RRULE:FREQ=WEEKLY;BYDAY=SA,SU",
        ),
        # MONTHLY recurring events - Sự kiện lặp lại hàng tháng
        (
            "Tạo lịch họp giao ban hàng tháng vào ngày 5 lúc 9 giờ sáng.",
            today.replace(day=5),
            today.replace(day=5),
            "09:00:00",
            "09:00:00",
            "RRULE:FREQ=MONTHLY;BYMONTHDAY=5",
        ),
        (
            "Đặt lịch đi khám sức khỏe định kỳ hàng tháng vào ngày 10 lúc 14:00.",
            today.replace(day=10),
            today.replace(day=10),
            "14:00:00",
            "14:00:00",
            "RRULE:FREQ=MONTHLY;BYMONTHDAY=10",
        ),
        (
            "Lên lịch họp quản lý mỗi tháng vào thứ Hai đầu tiên lúc 10:00.",
            get_valid_weekday(weekdays[0]),
            get_valid_weekday(weekdays[0]),
            "10:00:00",
            "10:00:00",
            "RRULE:FREQ=MONTHLY;BYDAY=1MO",
        ),
        (
            "Tạo lịch đi hiến máu mỗi 3 tháng vào ngày 15.",
            today.replace(day=15),
            today.replace(day=15),
            "09:00:00",
            "09:00:00",
            "RRULE:FREQ=MONTHLY;INTERVAL=3;BYMONTHDAY=15",
        ),
        (
            "Đặt lịch họp tổng kết hàng tháng vào ngày cuối cùng của tháng lúc 16:00.",
            today.replace(day=calendar.monthrange(today.year, today.month)[1]),
            today.replace(day=calendar.monthrange(today.year, today.month)[1]),
            "16:00:00",
            "16:00:00",
            "RRULE:FREQ=MONTHLY;BYMONTHDAY=-1",
        ),
        # YEARLY recurring events - Sự kiện lặp lại hàng năm
        (
            "Tạo lịch kỷ niệm ngày cưới hàng năm vào ngày 12 tháng 8 lúc 18:00.",
            today.replace(day=12, month=8),
            today.replace(day=12, month=8),
            "18:00:00",
            "18:00:00",
            "RRULE:FREQ=YEARLY;BYMONTHDAY=12;BYMONTH=8",
        ),
        (
            "Đặt lịch họp cổ đông thường niên vào ngày 15 tháng 3 mỗi năm lúc 9:00.",
            today.replace(day=15, month=3),
            today.replace(day=15, month=3),
            "09:00:00",
            "09:00:00",
            "RRULE:FREQ=YEARLY;BYMONTHDAY=15;BYMONTH=3",
        ),
        (
            "Lên lịch tổ chức sinh nhật công ty hàng năm vào ngày 20 tháng 10 lúc 15:00.",
            today.replace(day=20, month=10),
            today.replace(day=20, month=10),
            "15:00:00",
            "15:00:00",
            "RRULE:FREQ=YEARLY;BYMONTHDAY=20;BYMONTH=10",
        ),
        (
            "Tạo nhắc nhở nộp thuế thu nhập cá nhân hàng năm trước ngày 30 tháng 3.",
            today.replace(day=30, month=3),
            today.replace(day=30, month=3),
            "09:00:00",
            "09:00:00",
            "RRULE:FREQ=YEARLY;BYMONTHDAY=30;BYMONTH=3",
        ),
        (
            "Đặt lịch kỷ niệm ngày thành lập Đảng mỗi năm vào ngày 3 tháng 2.",
            today.replace(day=3, month=2),
            today.replace(day=3, month=2),
            "00:00:00",
            "23:59:59",
            "RRULE:FREQ=YEARLY;BYMONTHDAY=3;BYMONTH=2",
        ),
        # Sự kiện lặp lại có địa điểm
        (
            "Tạo lịch tập yoga hàng tuần vào thứ Ba và thứ Năm lúc 18:00 tại CLB Sức Khỏe Tươi Mới.",
            get_valid_weekday(weekdays[1]),
            get_valid_weekday(weekdays[1]),
            "18:00:00",
            "18:00:00",
            "RRULE:FREQ=WEEKLY;BYDAY=TU,TH",
        ),
        (
            "Đặt lịch đi khám sức khỏe định kỳ 3 tháng một lần tại Bệnh viện Việt Đức vào ngày 10 lúc 8:00 sáng.",
            today.replace(day=10),
            today.replace(day=10),
            "08:00:00",
            "08:00:00",
            "RRULE:FREQ=MONTHLY;INTERVAL=3;BYMONTHDAY=10",
        ),
        (
            "Lên lịch họp nhóm dự án hàng tuần tại phòng 305 tòa nhà Innovation vào thứ Hai lúc 14:00.",
            get_valid_weekday(weekdays[0]),
            get_valid_weekday(weekdays[0]),
            "14:00:00",
            "14:00:00",
            "RRULE:FREQ=WEEKLY;BYDAY=MO",
        ),
        (
            "Tạo lịch tham dự buổi đào tạo kỹ năng mềm mỗi thứ Sáu đầu tiên hàng tháng tại Trung tâm Phát triển nhân tài lúc 9:00.",
            get_valid_weekday(weekdays[4]),
            get_valid_weekday(weekdays[4]),
            "09:00:00",
            "09:00:00",
            "RRULE:FREQ=MONTHLY;BYDAY=1FR",
        ),
        (
            "Đặt lịch đón con mỗi ngày tại trường Tiểu học Xuân Phương vào lúc 17:00.",
            today,
            today,
            "17:00:00",
            "17:00:00",
            "RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR",
        ),
        # Sự kiện đặc biệt
        (
            "Tạo lịch họp giao ban mỗi thứ Hai, thứ Tư và thứ Sáu hàng tuần tại Văn phòng Tầng 15 vào lúc 8:30 sáng.",
            get_valid_weekday(weekdays[0]),
            get_valid_weekday(weekdays[0]),
            "08:30:00",
            "08:30:00",
            "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR",
        ),
        (
            "Đặt lịch gọi điện cho bố mẹ mỗi Chủ Nhật lúc 20:00 tối.",
            get_valid_weekday(weekdays[6]),
            get_valid_weekday(weekdays[6]),
            "20:00:00",
            "20:00:00",
            "RRULE:FREQ=WEEKLY;BYDAY=SU",
        ),
        (
            "Tạo lịch dọn dẹp căn hộ vào Chủ Nhật đầu tiên mỗi tháng từ 9:00 sáng đến 12:00 trưa.",
            get_valid_weekday(weekdays[6]),
            get_valid_weekday(weekdays[6]),
            "09:00:00",
            "12:00:00",
            "RRULE:FREQ=MONTHLY;BYDAY=1SU",
        ),
        (
            "Lên lịch kiểm tra xe hai tháng một lần vào ngày 25 lúc 14:00 tại Gara Thành Công.",
            today.replace(day=25),
            today.replace(day=25),
            "14:00:00",
            "14:00:00",
            "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=25",
        ),
        (
            "Tạo lịch mua sắm hàng tháng vào thứ Bảy cuối cùng của tháng tại siêu thị Vinmart từ 10:00 đến 12:00.",
            get_valid_weekday(weekdays[5]),
            get_valid_weekday(weekdays[5]),
            "10:00:00",
            "12:00:00",
            "RRULE:FREQ=MONTHLY;BYDAY=-1SA",
        ),
    ],
)
def test_extract_event_recurrence(
    prompt, start_date, end_date, start_time, end_time, rrule
):
    result = extract_datetime_from_text(prompt, True)
    datetime_ranges = result["datetime_ranges"][0]

    start_datetime = start_date.strftime("%Y-%m-%d") + " " + start_time
    end_datetime = end_date.strftime("%Y-%m-%d") + " " + end_time

    assert (
        datetime_ranges["start_datetime"] == start_datetime
    ), f"Failed for input '{prompt}'. Expected start '{start_datetime}' but got '{datetime_ranges['start_datetime']}'"
    assert (
        datetime_ranges["end_datetime"] == end_datetime
    ), f"Failed for input '{prompt}'. Expected end '{end_datetime}' but got '{datetime_ranges['end_datetime']}'"
    assert (
        datetime_ranges["rrules"] == rrule
    ), f"Failed for input '{prompt}'. Expected rrule '{rrule}' but got '{datetime_ranges['rrules']}'"

    # Sleep to avoid rate limiting with the LLM API
    time.sleep(4)


if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/create_event_recurrence.py"])
