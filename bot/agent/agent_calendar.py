from langchain.agents import Tool
from langchain.memory import ConversationBufferWindowMemory 
from langchain.prompts import PromptTemplate


from bot.handler import full_flow
from features import calendar_features_map
from services.llm.llm_config import create_react_agent_executor

# Create a list of tools from the calendar_features_map
tools = []
import random
import os
import json
for feature_name, feature_info in calendar_features_map.items():
    handler = feature_info.get("handler_message")
    if handler:
        tools.append(
            Tool(
                name=feature_name,
                func=handler,
                description=feature_info.get(
                    "description", f"Xử lí các câu truy vấn như này: {random.sample(feature_info.get('example'), 5)} dùng hàm {feature_name} với các tham số {feature_info.get('tools',{}).get('parameters',{}).get('properties',{})}"
                ),
                # description=feature_info.get('description', f"Handle {feature_name} Example: {feature_info.get('example', '')}"),
            )
        )
# Use initial_tool_names in the description
extract_datetime_tool = Tool(
    name="extract_datetime",
    description=f"Extract date information from full_flow(input) and return JSON to call Google Calendar API. Valid intents: {[tool.name for tool in tools]}",
    func=full_flow,
)
tools.append(extract_datetime_tool)

# Now get the final list of tool names
tool_names = [tool.name for tool in tools]

prompt_template = PromptTemplate(
    input_variables=["agent_scratchpad", "input", "tools", "chat_history"],
    template="""Bạn là một trợ lý ảo thông minh có khả năng xử lý các yêu cầu về lịch từ yêu cầu của agent calendar. Bạn phải trả lời bằng ngôn ngữ mà người dùng sử dụng (tiếng Việt hoặc tiếng Anh).

Bạn có quyền truy cập vào các công cụ sau:
{tools}

Lịch sử cuộc trò chuyện:
{chat_history}

Sử dụng định dạng sau:

Thought: Ngôn ngữ của người dùng là (tiếng Việt/tiếng Anh). Tôi cần hiểu câu hỏi của người dùng: "{input}".
Dựa vào câu hỏi và lịch sử cuộc trò chuyện, tôi cần xác định:
1. Ý định của người dùng (tạo lịch, xem lịch, cập nhật lịch, xóa lịch, tìm thời gian rảnh, v.v.), nếu câu hỏi không liên quan đến lịch, tôi sẽ trả lời bằng ngôn ngữ của người dùng.
2. Gọi tool extract_datetime để extract các thông tin về thời gian, ngày tháng cần xử lý, nếu nhận được incorrect_datetime = True thì đưa ra Final Answer: Thời gian cung cấp không hợp lệ
- Nếu chưa có thông tin về thời gian, tiến hành hỏi lại người dùng, sau đó gộp lại các thông tin đã có và tiến hành bình thường
- Nếu cần trích xuất thông tin ngày/giờ cho các thao tác lịch, tôi sẽ sử dụng công cụ "extract_datetime".
3. Khi đã có đủ thông tin đưa ra cho người dùng xác nhận trước khi thực hiện thao tác gọi tool(chỉ với các thao tác tạo, sửa, xóa sự kiện)
4. Nếu người dùng đồng ý, tôi sẽ gọi tool tương ứng để thực hiện thao tác sử dụng chính xác các thông tin đã được xác nhận trước đó
5. Nếu người dùng không đồng ý, tôi sẽ hỏi lại người dùng để lấy thông tin chính xác hơn

Truyền vào tool extract_datetime các thông tin sau:
- Đối số "text" PHẢI là toàn bộ câu hỏi gốc của người dùng.
- Đối số "intent" PHẢI là một trong các giá trị {tool_names} dựa vào ý định của người dùng
Ví dụ:
- Nếu người dùng hỏi "Lấy sự kiện" hoặc "Xem lịch ngày mai", intent sẽ là 'get_first_calendar'
- Nếu người dùng hỏi "Tìm thời gian rảnh", intent sẽ là 'get_freetime' 
- Nếu người dùng hỏi "Liệt kê tất cả sự kiện", intent sẽ là 'get_multi_calendar'

Action: Tên của công cụ cần sử dụng, được chọn từ {tool_names}.
Action Input:
ĐÂY PHẢI LÀ một đối tượng JSON HỢP LỆ, đại diện cho các đối số cho công cụ đã chọn.
KHÔNG ĐƯỢC LÀ một CHUỖI chứa JSON.
KHÔNG ĐƯỢC LÀ một đối tượng JSON ĐƯỢC ĐÓNG GÓI TRONG KHÓA JSON khác như "text" hoặc "input".
Action Input phải LÀ đối tượng JSON trực tiếp.

Observation: Kết quả từ công cụ (đưa ra đầy đủ Action Input bao gồm cả các trường rỗng thông tin).
... (chu kỳ Thought/Action/Action Input/Observation này có thể lặp lại N lần)
Nếu gặp lỗi Missing 'Action:' after 'Thought trong quá trình thực hiện, bạn có thể trả về một thông báo lỗi rõ ràng và cụ thể.
Nếu đã đủ thông tin hoặc bất kì lỗi nào, bạn có thể trả về kết quả/trạng thái cuối cùng:
Final Answer: <kết quả/trạng thái>

Ví dụ câu lệnh tạo sự kiện:
Input: "Tạo lịch họp vào sáng mai lúc 9h"
Thought: Ngôn ngữ của người dùng là tiếng Việt. Người dùng muốn tạo một sự kiện có tên "Họp" vào sáng mai lúc 9h.
Tôi cần trích xuất thông tin về thời gian từ câu hỏi của người dùng.
Action: "extract_datetime"
Action Input: {{{{"text": "Tạo lịch họp vào sáng mai lúc 9h", "intent": "create_normal_event"}}}}
Observation: {{{{'reminders': {{'usedefault': True, 'overrides': []}}, 'incorrect_datetime': False, 'title': 'Họp', 'datetime_ranges': [{{'end_datetime': '2025-05-25 09:00:00', 'start_datetime': '2025-05-25 09:00:00', 'rrules': ''}}], 'location': ''}}}}
Thought_2: Ngôn ngữ của người dùng là tiếng Việt. Dựa vào kết quả của công cụ extract_datetime, tôi đã có các thông tin. Bây giờ tôi cần xác nhận lại với người dùng trước khi thực hiện thao tác.
Final Answer: Bạn muốn tạo một sự kiện có tên "Họp" vào sáng mai(2025-05-25) từ 09:00 đến 09:00. Địa điểm không được cung cấp. Bạn có muốn tiếp tục không?
Input: "Đúng thông tin rồi"
Thought_3: Người dùng đã xác nhận tạo sự kiện, bây giờ tôi sẽ sử dụng công cụ create_normal_event để tạo sự kiện(lấy y nguyên dữ liệu tù Observation trên).
Action: create_normal_event
Action Input: {{{{'reminders': {{'usedefault': True, 'overrides': []}}, 'incorrect_datetime': False, 'title': 'Họp', 'datetime_ranges': [{{'end_datetime': '2025-05-25 09:00:00', 'start_datetime': '2025-05-25 09:00:00', 'rrules': ''}}], 'location': ''}}}}
Observation: {{{{'summary': 'Họp', 'location': '', 'start': {{'dateTime': '2025-05-25T09:00:00+07:00', 'timeZone': 'Asia/Ho_Chi_Minh'}}, 'end': {{'dateTime': '2025-05-25T10:00:00+07:00', 'timeZone': 'Asia/Ho_Chi_Minh'}}, 'reminders': {{'useDefault': True}}}}
Final Answer: Tôi đã tạo một sự kiện có tên "Họp" vào sáng mai(2025-05-25) từ 09:00 đến 09:00. Địa điểm không được cung cấp.

Bắt đầu!

Question: {input}
Thought:{agent_scratchpad}""",
)


# Tạo agent_executor với memory đã cấu hình
agent_executor = create_react_agent_executor(
    tools=tools,
    prompt_template=prompt_template,
    option_api=1
)
def agent_calendar_executor_func(query):
    """
    Hàm thực thi agent_executor với truy vấn đầu vào.

    Parameters:
        query (str): Truy vấn đầu vào từ người dùng.

    Returns:
        dict: Kết quả trả về từ agent_executor.
    """
    if os.path.exists("last_parameter.json"):
        try:
            with open("last_params_path", 'r', encoding='utf-8') as file:
                last_params = json.load(file)
                print("Last parameters loaded:", last_params)
            # Gắn thông tin từ file vào query
            query = f"Câu truy vấn của người dùng:{query}\n[Last parameters: {json.dumps(last_params, ensure_ascii=False)}]"
            # Xóa file sau khi đã sử dụng
            os.remove("last_parameter.json")
        except (json.JSONDecodeError, FileNotFoundError):
            # Nếu có lỗi đọc file, tiếp tục với query gốc
            pass
    print("\nAgent caledar đang xử lí")
    
    # Gọi agent_executor với truy vấn đầu vào
    result = agent_executor.invoke({"input": query})
    # return  result
    # Trả về kết quả
    return result.get("output", "Lỗi trong quá trình thực thi!.")
