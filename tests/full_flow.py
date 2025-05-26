import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

from bot import agent_calendar_executor_func
from bot.agent_intent import intent_model
# ['calendar', 'gmail','normal_message']
# Phân loại ý định của người dùng
prompt = "Tôi muốn tạo lịch họp vào sáng mai lúc 9h"
intent = intent_model(prompt)
flag_intent = ''
print(f"Ý định của người dùng: {intent}")

def phanloai_intent(intent):
    if intent.get('intent') == "calendar":
        # Nếu ý định là tạo sự kiện, gọi hàm agent_calendar_executor_func
        result = agent_calendar_executor_func(prompt)
        print("Kết quả từ agent_calendar_executor_func:", result)
    elif intent.get('intent') == "gmail":
        # Nếu ý định là liên quan đến Gmail, xử lý tương ứng
        print("Ý định là liên quan đến Gmail, cần xử lý thêm.")
    elif intent.get('intent') == "normal_message":
        # Nếu ý định là tin nhắn thông thường, xử lý tương ứng
        print("Ý định là tin nhắn thông thường, cần xử lý thêm.")
    else:
        print("Không xác định được ý định của người dùng.")
        
        
query = [
    "Tạo lịch họp vào sáng mai lúc 9h",
    "Đúng rồi"
]
for i in query:
    # Nhập truy vấn từ người dùng
    print(f"\nTruy vấn từ người dùng: {i}")
    print("flag_intent", flag_intent)
    if flag_intent != '':
        # Phân loại ý định của người dùng
        intent = flag_intent
    else:
        # Phân loại ý định của người dùng
        intent = intent_model(i)
        flag_intent = intent

    print(f"Ý định của người dùng: {intent}")
    # Xử lý theo ý định đã phân loại
    phanloai_intent(intent)
    
    print("\n" + "-"*50)