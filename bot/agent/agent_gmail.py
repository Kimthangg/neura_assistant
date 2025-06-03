from langchain.agents import Tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate


from services.llm.llm_config import create_react_agent_executor

from bot.handler import full_flow
from features import gmail_features_map
from services.llm.llm_config import create_react_agent_executor
# Create a list of tools from the gmail_features_map
tools = []
import random
import os
import json

for feature_name, feature_info in gmail_features_map.items():
    handler = feature_info.get("handler_message")
    if handler:
        tools.append(
            Tool(
                name=feature_name,
                func=handler,
                description=feature_info.get(
                    "description", f"Xử lí các câu truy vấn như này: {random.sample(feature_info.get('example'), 5)} dùng hàm {feature_name} với các tham số {feature_info.get('tools',{}).get('parameters',{}).get('properties',{})}"
                ),
            )
        )

# Use initial_tool_names in the description
extract_datetime_tool = Tool(
    name="extract_datetime",
    description=f"Extract date information from full_flow(input) and return JSON to call Gmail API. Valid intents: {[tool.name for tool in tools]}",
    func=full_flow,
)
tools.append(extract_datetime_tool)

# Now get the final list of tool names
tool_names = [tool.name for tool in tools]

prompt_template = PromptTemplate(
    input_variables=["agent_scratchpad", "input", "tools", "chat_history"],
    template="""Bạn là một trợ lý ảo thông minh có khả năng xử lý các yêu cầu về Gmail từ yêu cầu của agent gmail. Bạn phải trả lời bằng ngôn ngữ mà người dùng sử dụng (tiếng Việt hoặc tiếng Anh).

Bạn có quyền truy cập vào các công cụ sau:
{tools}

Lịch sử cuộc trò chuyện:
{chat_history}

Sử dụng định dạng sau:

Thought: Ngôn ngữ của người dùng là (tiếng Việt/tiếng Anh). Tôi cần hiểu câu hỏi của người dùng: "{input}".
Dựa vào câu hỏi và lịch sử cuộc trò chuyện, tôi cần xác định:
1. Ý định của người dùng (tóm tắt email, tìm kiếm email, v.v.), nếu câu hỏi không liên quan đến email, tôi sẽ trả lời bằng ngôn ngữ của người dùng.
2. Gọi tool extract_datetime để extract các thông tin về thời gian, ngày tháng cần xử lý, nếu nhận được incorrect_datetime = True thì đưa ra Final Answer: Thời gian cung cấp không hợp lệ
- Nếu chưa có thông tin về thời gian, tiến hành hỏi lại người dùng, sau đó gộp lại các thông tin đã có và tiến hành bình thường
- Nếu cần trích xuất thông tin ngày/giờ cho các thao tác email, tôi sẽ sử dụng công cụ "extract_datetime".
3. Khi đã có đủ thông tin, tôi sẽ gọi tool tương ứng để thực hiện thao tác sử dụng chính xác các thông tin đã được xác nhận.

Truyền vào tool extract_datetime các thông tin sau:
- Đối số "text" PHẢI là toàn bộ câu hỏi gốc của người dùng.
- Đối số "intent" PHẢI là một trong các giá trị {tool_names} dựa vào ý định của người dùng
Ví dụ:
- Nếu người dùng hỏi "Tóm tắt email trong tuần này", intent sẽ là 'summarize_emails'
- Nếu người dùng hỏi "Tìm email từ john@example.com", intent sẽ là 'summarize_emails'

Action: Tên của công cụ cần sử dụng, được chọn từ {tool_names}.
Action Input:
ĐÂY PHẢI LÀ một đối tượng JSON HỢP LỆ, đại diện cho các đối số cho công cụ đã chọn.
KHÔNG ĐƯỢC LÀ một CHUỖI chứa JSON.
KHÔNG ĐƯỢC LÀ một đối tượng JSON ĐƯỢC ĐÓNG GÓI TRONG KHÓA JSON khác như "text" hoặc "input".
Action Input phải LÀ đối tượng JSON trực tiếp.
ví dụ:
Action: extract_datetime
Action Input: {{"text": "Tóm tắt email hôm nay", "intent": "summarize_emails"}}

Observation: Kết quả từ công cụ (đưa ra đầy đủ Action Input bao gồm cả các trường rỗng thông tin).
... (chu kỳ Thought/Action/Action Input/Observation này có thể lặp lại N lần)
Nếu gặp lỗi Missing 'Action:' after 'Thought trong quá trình thực hiện, bạn có thể trả về một thông báo lỗi rõ ràng và cụ thể.
Nếu đã đủ thông tin hoặc bất kì lỗi nào, bạn có thể trả về kết quả cuối cùng:
Final Answer: <kết quả>
- Đối với tóm tắt email, bạn sẽ trả về bản tóm tắt, đồng thời nếu có các thông tin về ngày tháng, địa điểm, link cuộc họp trong nội dung email thì hãy đưa ra các thông tin đó cho người dùng biết.
- Nếu có nhiều email được tóm tắt, hãy đưa ra danh sách được đánh số (1,2,3,...) các email đã được tóm tắt.
- Kết quả bạn đưa ra để cho 1 agent khác xử lý tiếp, vì vậy hãy đảm bảo rằng kết quả FINAL ANSWER và sử dụng bởi agent khác.
Bắt đầu!

Question: {input}
Thought:{agent_scratchpad}""",
)
from langchain.memory import ConversationBufferWindowMemory
memory_gmail = ConversationBufferWindowMemory(
    memory_key="chat_history", 
    k=3, 
    return_messages=True,
)


def agent_gmail_executor_func(query,flag=False):
    """
    Hàm thực thi agent_executor với truy vấn đầu vào.

    Parameters:
        query (str): Truy vấn đầu vào từ người dùng.

    Returns:
        dict: Kết quả trả về từ agent_executor.
    """
    if flag:
        memory_gmail.clear()
    else:
        print("\nAgent Gmail đang xử lí")
        # Tạo agent_executor với memory đã cấu hình
        agent_executor = create_react_agent_executor(
            tools=tools,
            prompt_template=prompt_template,
            memory=memory_gmail,
            option_api=1
        )
        # Gọi agent_executor với truy vấn đầu vào
        result = agent_executor.invoke({"input": query})
        # Trả về kết quả
        return result.get("output", "Lỗi trong quá trình thực thi!.")
