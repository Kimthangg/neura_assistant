import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

from bot import agent_manager_executor_func, handle_tam

while True:
    # Nhập truy vấn từ người dùng
    query = input("Nhập truy vấn: ")
    if query.lower() == "exit":
        break

# queries = [
    # "Tóm tắt email ngày 09/5",
    # ""
#     "Tìm kiếm email từ người dùng cụ thể",
#     "Tóm tắt email từ người dùng cụ thể",
#     "Tìm kiếm email có từ khóa cụ thể",
#     "Tóm tắt email có từ khóa cụ thể",
# ]
# import time
# # Chạy từng truy vấn theo thứ tự và giữ nguyên bộ nhớ giữa các lần gọi
# for i, query in enumerate(queries):
#     print(f"\n--- Truy vấn {i+1}: {query} ---\n")
    result = handle_tam(query)
    print("\nFinal Answer:", result)
    print("\n" + "-"*50)
    # time.sleep(3)
