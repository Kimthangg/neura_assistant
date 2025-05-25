create_event_recurrence_example = [
    # ===== SỰ KIỆN LẶP LẠI THEO NGÀY TRONG TUẦN =====
    # Format: [hành động tạo lịch] + [tên sự kiện] + vào + [thứ trong tuần] + [tần suất] + lúc + [giờ]
    "Tạo lịch họp nhóm vào thứ Hai hàng tuần lúc 10:00.",
    "Lên lịch tập gym vào thứ Ba hàng tuần lúc 18:00.",
    "Đặt lịch học tiếng Anh vào thứ Tư hàng tuần lúc 19:00.",
    "Lên lịch gặp mentor vào thứ Năm hàng tuần lúc 14:00.",
    "Tạo sự kiện đọc sách vào thứ Sáu hàng tuần lúc 20:00.",
    "Đặt lịch đi siêu thị vào thứ Bảy hàng tuần lúc 9:00.",
    "Lên lịch dọn dẹp nhà cửa vào Chủ Nhật hàng tuần lúc 15:00.",
    "Tạo lịch gọi điện về cho gia đình vào thứ Bảy hàng tuần lúc 20:00.",
    "Đặt lịch cập nhật công việc vào thứ Hai hàng tuần lúc 8:30.",
    "Tạo sự kiện họp kế hoạch vào thứ Sáu hàng tuần lúc 16:00.",
    # ===== SỰ KIỆN LẶP LẠI THEO THÁNG =====
    # Format: [hành động tạo lịch] + [tên sự kiện] + vào ngày + [số ngày] + [tần suất tháng] + lúc + [giờ]
    "Tạo lịch thanh toán hóa đơn vào ngày 5 hàng tháng lúc 10:00.",
    "Lên lịch kiểm tra sức khỏe vào ngày 15 hàng tháng lúc 9:00.",
    "Đặt lịch họp toàn công ty vào ngày 1 hàng tháng lúc 14:00.",
    "Tạo sự kiện báo cáo tiến độ vào ngày 20 hàng tháng lúc 17:00.",
    "Đặt lịch học nâng cao kỹ năng vào ngày 10 hàng tháng lúc 19:00.",
    "Lên lịch kiểm tra tài chính cá nhân vào ngày 25 hàng tháng lúc 8:00.",
    "Tạo sự kiện backup dữ liệu vào ngày cuối cùng của tháng lúc 23:00.",
    "Lên lịch bảo trì xe vào ngày 7 hàng tháng lúc 9:00.",
    "Đặt lịch cập nhật hồ sơ cá nhân vào ngày 3 hàng tháng lúc 15:00.",
    "Tạo lịch họp nhóm dự án vào ngày 12 hàng tháng lúc 13:00.",
    # ===== SỰ KIỆN LẶP LẠI THEO NĂM =====
    # Format: [hành động tạo lịch] + [tên sự kiện] + vào ngày + [ngày tháng] + [tần suất năm] + lúc + [giờ]
    "Lên lịch họp tổng kết năm vào ngày 31 tháng 12 lúc 15:00.",
    "Tạo lịch kỷ niệm ngày cưới vào ngày 20 tháng 6 hàng năm lúc 19:00.",
    "Đặt lịch chúc mừng sinh nhật sếp vào ngày 5 tháng 9 hàng năm lúc 10:00.",
    "Lên lịch kiểm tra sức khỏe tổng quát vào ngày 1 tháng 3 hàng năm lúc 9:00.",
    "Tạo sự kiện gia đình đi du lịch vào ngày 15 tháng 7 hàng năm lúc 8:00.",
    "Đặt lịch họp cổ đông vào ngày 25 tháng 4 hàng năm lúc 14:00.",
    "Lên lịch viết mục tiêu năm mới vào ngày 31 tháng 12 hàng năm lúc 18:00.",
    "Tạo sự kiện tổng kết tài chính vào ngày 30 tháng 11 hàng năm lúc 16:00.",
    "Đặt lịch tiêm vaccine nhắc lại vào ngày 10 tháng 5 hàng năm lúc 9:30.",
    "Lên lịch đổi mật khẩu các tài khoản quan trọng vào ngày 1 tháng 6 hàng năm lúc 12:00.",
    # ===== SỰ KIỆN LẶP LẠI THEO SỐ TUẦN NHẤT ĐỊNH =====
    # Format: [hành động tạo lịch] + [tên sự kiện] + mỗi + [số] + tuần + vào + [thứ trong tuần] + lúc + [giờ]
    "Tạo lịch họp dự án mỗi 2 tuần vào thứ Hai lúc 10:00.",
    "Đặt lịch kiểm tra tiến độ công việc mỗi 3 tuần vào thứ Ba lúc 14:00.",
    "Lên lịch học nâng cao kỹ năng mỗi 4 tuần vào thứ Tư lúc 19:00.",
    "Tạo sự kiện kiểm tra định kỳ sản phẩm mỗi 6 tuần vào thứ Năm lúc 15:00.",
    "Đặt lịch cập nhật báo cáo tài chính mỗi 8 tuần vào thứ Sáu lúc 9:00.",
    "Lên lịch họp nhóm chiến lược mỗi 5 tuần vào thứ Hai lúc 11:00.",
    "Tạo sự kiện xem xét hợp đồng mới mỗi 7 tuần vào thứ Ba lúc 13:00.",
    "Đặt lịch bảo trì thiết bị mỗi 10 tuần vào thứ Tư lúc 16:00.",
    "Lên lịch kiểm tra bảo mật hệ thống mỗi 12 tuần vào thứ Năm lúc 9:00.",
    "Tạo sự kiện đào tạo nhân viên mới mỗi 9 tuần vào thứ Sáu lúc 14:00.",
]

create_event_example = [
    # ===== SỰ KIỆN CÓ NGÀY GIỜ CỤ THỂ =====
    # Format: [hành động tạo lịch] + [tên sự kiện] + vào + [thời gian cụ thể] + lúc + [giờ]
    "Tạo sự kiện họp nhóm vào ngày mai lúc 15:00.",
    "Đặt lịch ăn tối với bạn vào thứ Sáu tuần này lúc 19:30.",
    "Lên lịch gặp khách hàng vào ngày 25 tháng 3 lúc 10 giờ sáng.",
    "Lên lịch đi phỏng vấn vào thứ Ba lúc 14:00.",
    "Đặt lịch kiểm tra sức khỏe vào 8 giờ sáng thứ Tư.",
    "Tạo lịch đi chụp ảnh cưới vào chủ nhật tuần này lúc 16:00.",
    "Lên lịch đi làm căn cước công dân vào ngày 10 tháng 6 lúc 8:00.",
    # ===== SỰ KIỆN CÓ KHOẢNG THỜI GIAN =====
    # Format: [hành động tạo lịch] + [tên sự kiện] + vào + [ngày] + từ + [giờ bắt đầu] + đến + [giờ kết thúc]
    "Đặt lịch dạy kèm toán cho em tôi vào thứ Sáu từ 18:00 đến 20:00.",
    "Đặt lịch họp nhóm từ 9 giờ sáng đến 11 giờ trưa ngày 20/04/2025.",
    "Hãy đặt lịch cho buổi học lập trình từ 20:00 đến 22:00 vào Chủ Nhật.",
    "Lên lịch làm bài kiểm tra thử TOEIC vào Chủ Nhật từ 14:00 đến 16:00.",
    "Tạo sự kiện đi du lịch từ ngày 1 đến ngày 5 tháng 8.",
    # ===== SỰ KIỆN CÓ ĐỊA ĐIỂM CỤ THỂ - Y TẾ =====
    # Format: [hành động tạo lịch] + [tên sự kiện y tế] + tại + [địa điểm y tế] + vào + [thời gian] + lúc + [giờ]
    "Tạo lịch đi khám bệnh tại Bệnh viện Bạch Mai vào 9:00 sáng mai.",
    "Lên lịch hẹn gặp bác sĩ nha khoa ở phòng khám Định Công lúc 10:00 ngày 10/04.",
    "Tạo sự kiện kiểm tra sức khỏe tổng quát tại Vinmec lúc 7:30 sáng thứ Ba tuần tới.",
    "Đặt lịch tiêm vaccine tại Bệnh viện Nhi Trung Ương vào 8:00 ngày 15/04.",
    "Lên lịch tập yoga ở phòng tập GymFit vào 6:00 sáng thứ Hai.",
    # ===== SỰ KIỆN CÓ ĐỊA ĐIỂM CỤ THỂ - GIẢI TRÍ =====
    # Format: [hành động tạo lịch] + [tên sự kiện giải trí] + tại + [địa điểm giải trí] + vào/lúc + [thời gian]
    "Hẹn đi karaoke với nhóm bạn tại quán King Karaoke lúc 19:30 thứ Bảy.",
    "Tạo lịch tham gia triển lãm nghệ thuật tại bảo tàng Mỹ Thuật vào 14:00 thứ Sáu.",
    "Lên lịch đi xem kịch tại Nhà hát Tuổi Trẻ vào 19:00 ngày 10/04.",
    "Hẹn đi chơi công viên Yên Sở vào 8:00 sáng thứ Bảy.",
    "Tạo sự kiện tham gia buổi hòa nhạc tại Trung tâm Hội nghị Quốc gia vào 20:00 ngày 20/04.",
    # ===== SỰ KIỆN CÓ ĐỊA ĐIỂM CỤ THỂ - XÃ HỘI/GIA ĐÌNH =====
    # Format: [hành động tạo lịch] + [tên sự kiện xã hội/gia đình] + tại + [địa điểm] + vào + [thời gian] + lúc + [giờ]
    "Hẹn ăn tối với gia đình tại nhà hàng Sen Tây Hồ vào 19:00 thứ Sáu.",
    "Lên lịch tổ chức sinh nhật cho em trai tại nhà vào 18:00 ngày 15/04.",
    "Tạo sự kiện đi du lịch Hạ Long, xuất phát lúc 6:00 sáng thứ Bảy tuần này.",
    "Hẹn họp lớp tại quán nướng Gogi vào 12:00 trưa Chủ Nhật.",
    "Đặt lịch đi thăm ông bà ở quê vào 9:00 sáng thứ Bảy.",
]

# import random

# print(random.sample(create_event_example, 5))
