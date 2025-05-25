import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))


# Tạo sự kiên
# print(full_flow("Tạo lịch học IELTS từ 7 giờ đến 9 giờ tối thứ Sáu tại trung tâm IELTS Thầy Long"))
# print(full_flow("Tạo lịch học TOEIC từ 5 giờ đến 10 giờ tối tại trung tâm Toeic Thầy Long vào thứ 5 tuần này"))
# print(full_flow("Tạo lịch đi siêu thị mỗi thứ Bảy lúc 17:00."))
# print(full_flow("Tạo lịch làm bài test TOEIC tại trung tâm Toeic A vào 16:00 ngày 30/04."))
# #Lấy sự kiện đầu tiên
# print(full_flow("Hôm nay tôi có lịch từ mấy giờ?"))
# print(full_flow("Ngày mai sự kiện bắt đầu lúc mấy giờ?"))
# #Lấy thời gian rảnh
# print(full_flow("Tìm thời gian rảnh của tôi trong tuần này"))
# print(full_flow("Ngày mai tôi có thời gian trống không?"))
# #Lấy nhiều sự kiên
# print(full_flow("Lịch của tôi ngày mai có gì?"))
# #Sửa sự kiện
# print(full_flow("Sửa lịch học IELTS từ 7 giờ đến 9 giờ tối thứ Sáu tại trung tâm IELTS Thầy Long thành 8 giờ đến 10 giờ tối"))
# #Xóa sự kiện
# print(full_flow("Xóa lịch học IELTS của tôi từ 8 giờ đến 10 giờ tối thứ Sáu tại trung tâm IELTS Thầy Long"))


# data = {
#     'intent': 'update_event',  # Adding proper intent
#      "datetime_ranges": [
#        {
#          "start_datetime": "2025-04-20 08:00:00",
#          "end_datetime": "2025-04-20 08:00:00",
#          "start_new": "2025-04-20 15:00:00",
#          "end_new": "2025-04-20 15:00:00"
#        }
#      ]
#    }
# # print(data['incorrect_datetime'])
# from features.update_calendar.handler import update_event_api
# print(update_event_api(data))
