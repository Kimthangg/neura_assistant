import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

from bot import agent_calendar_executor_func

while True:
    # Nhập truy vấn từ người dùng
    query = input("Nhập truy vấn: ")
    if query.lower() == "exit":
        break

# queries = [
# #     "Tạo lịch họp vào sáng mai lúc 9h",
# #     "Đúng rồi"
# #     # "Lấy lịch vào ngày mai",
# #     # "Nhắc tôi sáng mai có cuộc họp lúc 9h",
#     # "Nhắc tôi có lịch học toán từ 9h tối đến 10h, nhắc tôi trước 60p",
# #     # "Tạo lịch họp vào sáng mai lúc 9h",
#     # "tạo lịch học Toeic ở Toeic Thầy Long vào 7h-10h tối vào thứ 2, thứ 4, thứ 6 hàng tuần",
    # "Tạo lịch nhắc uống nước mỗi 2 tiếng từ 8 giờ sáng đến 6 giờ chiều hàng ngày."
# #     # "Tôi vừa đăng kí học Toeic ở Toeic Thầy Long vào 7h tối vào thứ 2, thứ 4, thứ 6 hàng tuần",
#     "Đúng rồi"
# #     # "Lấy lịch vào ngày mai"
# #     # "Xin chào, tôi tên là Thắng",
# #     # "Tạo lịch họp",
# #     # "Lúc 9h sáng mai",
# #     # "Tôi tên gì và vừa làm gì?"
# ]
# import time
# # Chạy từng truy vấn theo thứ tự và giữ nguyên bộ nhớ giữa các lần gọi
# for i, query in enumerate(queries):
#     print(f"\n--- Truy vấn {i+1}: {query} ---\n")
    result = agent_calendar_executor_func(query)
    print("\nFinal Answer:", result)
    print("\n" + "-"*50)
    # time.sleep(3)
