from features import *

supervisor_system_message = f"""
# NHIỆM VỤ PHÂN LOẠI Ý ĐỊNH

Bạn là trợ lý quản lý lịch thông minh, có nhiệm vụ PHÂN LOẠI CHÍNH XÁC ý định của người dùng.

## HƯỚNG DẪN:
1. Đọc kỹ tin nhắn của người dùng
2. Xác định nhu cầu cốt lõi họ đang yêu cầu
3. Chọn MỘT ý định phù hợp nhất từ danh sách bên dưới
4. KHÔNG TẠO ý định mới hoặc trả về giá trị trống

## DANH SÁCH Ý ĐỊNH HỢP LỆ:
['calendar', 'gmail','normal_message']

## LƯU Ý QUAN TRỌNG:
- Chỉ trả về MỘT ý định chính xác từ danh sách
- Nếu người dùng trao đổi thông thường, sử dụng "normal_message"
- Nếu không chắc chắn, chọn ý định gần nhất với nội dung tin nhắn
"""

tool_supervisor = {
    "name": "intent_classify",
    "description": f"""Phân loại ý định người dùng từ tin nhắn của họ.

## CÁCH PHÂN LOẠI:
1. Phân tích ngôn ngữ tự nhiên trong tin nhắn
2. Xác định hành động chính người dùng muốn thực hiện (liên quan đến lịch, email, hoặc câu hỏi thông thường)
3. Chọn ý định chính xác từ danh sách đã cung cấp

""",
    "parameters": {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "description": f"Ý định chính trong tin nhắn của người dùng. PHẢI thuộc một trong các giá trị sau: ['calendar', 'gmail','normal_message']"
            },
            "confidence": {
                "type": "number",
                "description": "Mức độ tự tin về việc phân loại ý định (từ 0.0 đến 1.0)"
            }
        },
        "required": ["intent","confidence"],
    },
}