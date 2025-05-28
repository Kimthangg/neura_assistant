import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import warnings

import pytest

warnings.filterwarnings("ignore")
import time

from bot.agent.create_event.datetime_extraction import (
    extract_datetime_from_text,
)
from utils import *

# Default time
today, tomorrow = get_today_tomorrow("Asia/Ho_Chi_Minh")

weekdays = get_weekdays_context()


@pytest.mark.parametrize(
    "prompt, start_date, end_date, start_time, end_time",
    [
        # Có ngày giờ cụ thể
        (
            "Tạo sự kiện họp nhóm vào ngày mai lúc 15:00.",
            tomorrow,
            tomorrow,
            "15:00:00",
            "15:00:00",
        ),
        # ("Đặt lịch ăn tối với bạn vào thứ Sáu tuần này lúc 19:30.", (weekdays[4]), (weekdays[4]), "19:30:00", "19:30:00"),
        (
            "Lên lịch gặp khách hàng vào ngày 25 tháng 3 lúc 10 giờ sáng.",
            today.replace(day=25, month=3),
            today.replace(day=25, month=3),
            "10:00:00",
            "10:00:00",
        ),
        # ("Lên lịch đi phỏng vấn vào thứ Ba lúc 14:00.", (weekdays[1]), (weekdays[1]), "14:00:00", "14:00:00"),
        # ("Đặt lịch kiểm tra sức khỏe vào 8 giờ sáng thứ Tư.", (weekdays[2]), (weekdays[2]), "08:00:00", "08:00:00"),
        # ("Tạo lịch đi chụp ảnh cưới vào chủ nhật tuần này lúc 16:00.", (weekdays[6]), (weekdays[6]), "16:00:00", "16:00:00"),
        (
            "Lên lịch đi làm căn cước công dân vào ngày 10 tháng 6 lúc 8:00.",
            today.replace(day=10, month=6),
            today.replace(day=10, month=6),
            "08:00:00",
            "08:00:00",
        ),
        # ("Đặt lịch dạy kèm toán cho em tôi vào thứ Sáu từ 18:00 đến 20:00.", (weekdays[4]), (weekdays[4]), "18:00:00", "20:00:00"),
        (
            "Đặt lịch họp nhóm từ 9 giờ sáng đến 11 giờ trưa ngày 20/04/2025.",
            today.replace(day=20, month=4),
            today.replace(day=20, month=4),
            "09:00:00",
            "11:00:00",
        ),
        # ("Hãy đặt lịch cho buổi học lập trình từ 20:00 đến 22:00 vào Chủ Nhật.", (weekdays[6]), (weekdays[6]), "20:00:00", "22:00:00"),
        # ("Lên lịch làm bài kiểm tra thử TOEIC vào Chủ Nhật từ 14:00 đến 16:00.", (weekdays[6]), (weekdays[6]), "14:00:00", "16:00:00"),
        (
            "Tạo sự kiện đi du lịch từ ngày 1 đến ngày 5 tháng 8.",
            today.replace(day=1, month=8),
            today.replace(day=5, month=8),
            "00:00:00",
            "23:59:59",
        ),
        # # Tuần này - đảm bảo có test case cho tất cả các ngày từ thứ Hai đến Chủ Nhật
        # ("Tạo sự kiện họp nhóm đồ án vào sáng thứ Hai tuần này lúc 9:00.", (weekdays[0]), (weekdays[0]), "09:00:00", "09:00:00"),
        # ("Tạo sự kiện thảo luận kế hoạch vào sáng thứ Ba tuần này lúc 9:00.", (weekdays[1]), (weekdays[1]), "09:00:00", "09:00:00"),
        # ("Đặt lịch đi ăn trưa với đồng nghiệp vào thứ Tư tuần này lúc 12:00.", (weekdays[2]), (weekdays[2]), "12:00:00", "12:00:00"),
        # ("Lên lịch tập gym vào chiều thứ Năm tuần này từ 17:30 đến 19:00.", (weekdays[3]), (weekdays[3]), "17:30:00", "19:00:00"),
        # ("Đặt lịch đi xem phim với bạn vào tối thứ Sáu tuần này lúc 20:00.", (weekdays[4]), (weekdays[4]), "20:00:00", "20:00:00"),
        # ("Tạo lịch đi mua sắm vào sáng thứ Bảy tuần này từ 10:00 đến 12:00.", (weekdays[5]), (weekdays[5]), "10:00:00", "12:00:00"),
        # ("Tạo lịch đi nhà thờ vào sáng Chủ Nhật tuần này lúc 8:00.", (weekdays[6]), (weekdays[6]), "08:00:00", "08:00:00"),
        # # Tuần tới - đảm bảo có test case cho tất cả các ngày từ thứ Hai đến Chủ Nhật
        # ("Lên lịch phỏng vấn việc làm vào thứ Hai tuần tới lúc 10:00 sáng.", (weekdays[7]), (weekdays[7]), "10:00:00", "10:00:00"),
        # ("Đặt lịch đi khám sức khỏe định kỳ vào thứ Ba tuần sau lúc 8:00.", (weekdays[8]), (weekdays[8]), "08:00:00", "08:00:00"),
        # ("Tạo sự kiện làm việc nhóm từ 14:00 đến 17:00 vào thứ Tư tuần tới.", (weekdays[9]), (weekdays[9]), "14:00:00", "17:00:00"),
        # ("Đặt lịch họp phòng ban vào sáng thứ Năm tuần tới lúc 9:30.", (weekdays[10]), (weekdays[10]), "09:30:00", "09:30:00"),
        # ("Lên lịch đi ăn tối với gia đình vào thứ Sáu tuần sau lúc 18:30.", (weekdays[11]), (weekdays[11]), "18:30:00", "18:30:00"),
        # ("Đặt lịch đi dã ngoại với bạn bè vào thứ Bảy tuần tới lúc 7:00 sáng.", (weekdays[12]), (weekdays[12]), "07:00:00", "07:00:00"),
        # ("Tạo lịch đi chơi công viên giải trí vào Chủ Nhật tuần tới lúc 9:00 sáng.", (weekdays[13]), (weekdays[13]), "09:00:00", "09:00:00"),
        # Test case với cả hai ngày cuối tuần
        (
            "Tạo sự kiện đi dã ngoại với bạn bè từ thứ Bảy đến Chủ Nhật tuần tới.",
            (weekdays[12]),
            (weekdays[13]),
            "00:00:00",
            "23:59:59",
        ),
        # Có địa điểm cụ thể
        (
            "Tạo lịch đi khám bệnh tại Bệnh viện Bạch Mai vào 9:00 sáng mai.",
            tomorrow,
            tomorrow,
            "09:00:00",
            "09:00:00",
        ),
        (
            "Lên lịch hẹn gặp bác sĩ nha khoa ở phòng khám Định Công lúc 10:00 ngày 10/04.",
            today.replace(day=10, month=4),
            today.replace(day=10, month=4),
            "10:00:00",
            "10:00:00",
        ),
        # ("Tạo sự kiện kiểm tra sức khỏe tổng quát tại Vinmec lúc 7:30 sáng thứ Ba tuần tới.", (weekdays[8]), (weekdays[8]), "07:30:00", "07:30:00"),
        (
            "Đặt lịch tiêm vaccine tại Bệnh viện Nhi Trung Ương vào 8:00 ngày 15/04.",
            today.replace(day=15, month=4),
            today.replace(day=15, month=4),
            "08:00:00",
            "08:00:00",
        ),
        # ("Lên lịch tập yoga ở phòng tập GymFit vào 6:00 sáng thứ Hai.", (weekdays[0]), (weekdays[0]), "06:00:00", "06:00:00"),
        # ("Hẹn đi karaoke với nhóm bạn tại quán King Karaoke lúc 19:30 thứ Bảy.", (weekdays[5]), (weekdays[5]), "19:30:00", "19:30:00"),
        # ("Tạo lịch tham gia triển lãm nghệ thuật tại bảo tàng Mỹ Thuật vào 14:00 thứ Sáu.", (weekdays[4]), (weekdays[4]), "14:00:00", "14:00:00"),
        (
            "Lên lịch đi xem kịch tại Nhà hát Tuổi Trẻ vào 19:00 ngày 10/04.",
            today.replace(day=10, month=4),
            today.replace(day=10, month=4),
            "19:00:00",
            "19:00:00",
        ),
        # ("Hẹn đi chơi công viên Yên Sở vào 8:00 sáng thứ Bảy.", (weekdays[5]), (weekdays[5]), "08:00:00", "08:00:00"),
        (
            "Tạo sự kiện tham gia buổi hòa nhạc tại Trung tâm Hội nghị Quốc gia vào 20:00 ngày 20/04.",
            today.replace(day=20, month=4),
            today.replace(day=20, month=4),
            "20:00:00",
            "20:00:00",
        ),
        # ("Hẹn ăn tối với gia đình tại nhà hàng Sen Tây Hồ vào 19:00 thứ Sáu.", (weekdays[4]), (weekdays[4]), "19:00:00", "19:00:00"),
        (
            "Lên lịch tổ chức sinh nhật cho em trai tại nhà vào 18:00 ngày 15/04.",
            today.replace(day=15, month=4),
            today.replace(day=15, month=4),
            "18:00:00",
            "18:00:00",
        ),
        # ("Tạo sự kiện đi du lịch Hạ Long, xuất phát lúc 6:00 sáng thứ Bảy tuần này.", (weekdays[5]), (weekdays[5]), "06:00:00", "06:00:00"),
        # ("Hẹn họp lớp tại quán nướng Gogi vào 12:00 trưa Chủ Nhật.", (weekdays[6]), (weekdays[6]), "12:00:00", "12:00:00"),
        # ("Đặt lịch đi thăm ông bà ở quê vào 9:00 sáng thứ Bảy.", (weekdays[5]), (weekdays[5]), "09:00:00", "09:00:00"),
        # Thêm test case có địa điểm cụ thể với thời gian trong tuần này và tuần tới - đảm bảo đủ các ngày
        (
            "Lên lịch tham dự hội thảo tại khách sạn Marriott vào thứ Hai tuần này lúc 13:30.",
            (weekdays[0]),
            (weekdays[0]),
            "13:30:00",
            "13:30:00",
        ),
        (
            "Đặt lịch họp kinh doanh tại văn phòng công ty vào thứ Ba tuần này lúc 14:00.",
            (weekdays[1]),
            (weekdays[1]),
            "14:00:00",
            "14:00:00",
        ),
        (
            "Tạo lịch dự buổi thuyết trình tại Đại học Bách Khoa vào thứ Tư tuần này lúc 15:00.",
            (weekdays[2]),
            (weekdays[2]),
            "15:00:00",
            "15:00:00",
        ),
        (
            "Lên lịch tham dự hội thảo tại khách sạn Marriott vào thứ Năm tuần này lúc 13:30.",
            (weekdays[3]),
            (weekdays[3]),
            "13:30:00",
            "13:30:00",
        ),
        (
            "Đặt lịch đi ăn tối với đối tác tại nhà hàng Ngon vào thứ Sáu tuần này lúc 18:00.",
            (weekdays[4]),
            (weekdays[4]),
            "18:00:00",
            "18:00:00",
        ),
        (
            "Đặt lịch đi chơi Vinpearl vào thứ Bảy tuần này từ 9:00 đến 17:00.",
            (weekdays[5]),
            (weekdays[5]),
            "09:00:00",
            "17:00:00",
        ),
        (
            "Đặt lịch dự tiệc cưới tại Trung tâm Tiệc cưới Diamond Palace vào Chủ Nhật tuần này lúc 18:00.",
            (weekdays[6]),
            (weekdays[6]),
            "18:00:00",
            "18:00:00",
        ),
        # Tuần tới với địa điểm
        (
            "Tạo sự kiện hội nghị khách hàng tại Khách sạn Intercontinental từ 8:00 đến 17:00 thứ Hai tuần tới.",
            (weekdays[7]),
            (weekdays[7]),
            "08:00:00",
            "17:00:00",
        ),
        (
            "Đặt lịch tham dự hội chợ việc làm tại Trung tâm Triển lãm vào thứ Ba tuần tới lúc 10:00.",
            (weekdays[8]),
            (weekdays[8]),
            "10:00:00",
            "10:00:00",
        ),
        (
            "Lên lịch tham dự cuộc họp Ban quản trị tại Tòa nhà Landmark 72 vào 9:00 sáng thứ Tư tuần sau.",
            (weekdays[9]),
            (weekdays[9]),
            "09:00:00",
            "09:00:00",
        ),
        (
            "Đặt lịch đi khám sức khỏe định kỳ tại bệnh viện Việt Đức vào thứ Năm tuần tới lúc 8:00.",
            (weekdays[10]),
            (weekdays[10]),
            "08:00:00",
            "08:00:00",
        ),
        (
            "Đặt lịch đi tham quan triển lãm công nghệ tại Trung tâm Hội chợ SECC vào thứ Sáu tuần tới từ 10:00 đến 16:00.",
            (weekdays[11]),
            (weekdays[11]),
            "10:00:00",
            "16:00:00",
        ),
        (
            "Lên lịch đi thăm Bảo tàng Lịch sử vào thứ Bảy tuần sau lúc 14:00.",
            (weekdays[12]),
            (weekdays[12]),
            "14:00:00",
            "14:00:00",
        ),
        (
            "Tạo lịch đi bơi tại Hồ bơi Mỹ Đình vào Chủ Nhật tuần tới lúc 16:00.",
            (weekdays[13]),
            (weekdays[13]),
            "16:00:00",
            "16:00:00",
        ),
    ],
)
def test_extract_event_normal(prompt, start_date, end_date, start_time, end_time):
    result = extract_datetime_from_text(prompt, False)
    datetime_ranges = result["datetime_ranges"][0]

    start_datetime = start_date.strftime("%Y-%m-%d") + " " + start_time
    end_datetime = end_date.strftime("%Y-%m-%d") + " " + end_time

    today_str = today.strftime("%Y-%m-%d")
    error_file = f"log/normal_event_{today_str}.txt"

    start_assertion = datetime_ranges["start_datetime"] == start_datetime
    end_assertion = datetime_ranges["end_datetime"] == end_datetime

    if not start_assertion or not end_assertion:
        with open(error_file, "a", encoding="utf-8") as f:
            if not start_assertion:
                f.write(f"Start datetime mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{start_datetime}'\n")
                f.write(f"  GenAI: '{datetime_ranges['start_datetime']}'\n\n")
            if not end_assertion:
                f.write(f"End datetime mismatch for: '{prompt}'\n")
                f.write(f"  Mong muốn: '{end_datetime}'\n")
                f.write(f"  GenAI: '{datetime_ranges['end_datetime']}'\n\n")

    assert (
        start_assertion
    ), f"Failed for input '{prompt}'. Mong muốn '{start_datetime}' but GenAI '{datetime_ranges['start_datetime']}'"
    assert (
        end_assertion
    ), f"Failed for input '{prompt}'. Mong muốn '{end_datetime}' but GenAI '{datetime_ranges['end_datetime']}'"
    time.sleep(4)


if __name__ == "__main__":
    pytest.main(["-sv", "tests/unittest/create_normal_event.py"])
