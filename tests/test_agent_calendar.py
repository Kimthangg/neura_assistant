import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))
from bot import agent_executor_func

queries = [
    "Tạo lịch họp vào sáng mai lúc 9h",
    # "Lấy lịch vào ngày mai",
    # "Nhắc tôi sáng mai có cuộc họp lúc 9h",
    # "Nhắc tôi có lịch học toán từ 9h tối đến 10h, nhắc tôi trước 60p",
    # "Tạo lịch họp vào sáng mai lúc 9h",
]
# Chạy từng truy vấn theo thứ tự và giữ nguyên bộ nhớ giữa các lần gọi
for i, query in enumerate(queries):
    print(f"\n--- Truy vấn {i+1}: {query} ---\n")
    result = agent_executor_func(query)
    print("\nFinal Answer:", result)
    print("\n" + "-"*50)

# while True:
#     # Nhập truy vấn từ người dùng
#     query = input("Nhập truy vấn: ")

#     # Thực hiện truy vấn và nhận kết quả
#     result = agent_executor_func(query)
#     # In kết quả
#     print("\nFinal Answer:", result)
#     print("\n" + "-"*50)