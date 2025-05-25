import os
import sys

from langchain.agents import Tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import json

from bot.handler import full_flow
from features import calendar_features_map
from services.llm.llm_config import create_react_agent_executor

# Create a list of tools from the calendar_features_map
tools = []
for feature_name, feature_info in calendar_features_map.items():
    handler = feature_info.get("handler_message")
    if handler:
        tools.append(
            Tool(
                name=feature_name,
                func=handler,
                description=feature_info.get("description", f"Handle {feature_name}"),
            )
        )

# Get initial tool names before adding extract_datetime_tool
initial_tool_names = [tool.name for tool in tools]


def extract_datetime_wrapper(action_input) -> str:
    """Wrapper to ensure correct argument passing to full_flow and JSON output."""
    try:
        payload = json.loads(action_input)
        result = full_flow(payload["text"], payload["intent"])
        print("Kết quả từ full_flow:", result)
        return result
    except Exception as e:
        return json.dumps({"error": f"full_flow failed: {e}"})


# Use initial_tool_names in the description
extract_datetime_tool = Tool(
    name="extract_datetime",
    description=f"Extract date information from input and return JSON to call Google Calendar API. Valid intents: {initial_tool_names}",
    func=extract_datetime_wrapper,
)
tools.append(extract_datetime_tool)

# Now get the final list of tool names
tool_names = [tool.name for tool in tools]


prompt_template = PromptTemplate(
    input_variables=["agent_scratchpad", "input", "tools"],
    template="""Bạn là một trợ lý ảo thông minh có khả năng xử lý các yêu cầu về lịch. Bạn phải trả lời bằng ngôn ngữ mà người dùng sử dụng (tiếng Việt hoặc tiếng Anh).

Bạn có quyền truy cập vào các công cụ sau:

{tools}

Lịch sử cuộc trò chuyện:
{chat_history}

Sử dụng định dạng sau:

Thought: Ngôn ngữ của người dùng là (tiếng Việt/tiếng Anh). Tôi cần hiểu câu hỏi của người dùng: "{input}".
Dựa vào câu hỏi và lịch sử cuộc trò chuyện, tôi cần xác định:
1. Ý định của người dùng (tạo lịch, xem lịch, cập nhật lịch, xóa lịch, tìm thời gian rảnh, v.v.)
2. Các thông tin về thời gian, ngày tháng cần xử lý, nếu nhận được incorrect_datetime = True thì đưa ra Final Answer: Thời gian cung cấp không hợp lệ
Nếu chưa có thông tin về thời gian, tiến hành hỏi lại người dùng, sau đó gộp lại các thông tin đã có và tiến hành bình thường
Nếu cần trích xuất thông tin ngày/giờ cho các thao tác lịch, tôi sẽ sử dụng công cụ "extract_datetime".
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
Ví dụ câu lệnh đầy đủ:
- Input: "Tạo lịch họp vào sáng mai"
- Ngôn ngữ của người dùng là tiếng Việt. Người dùng muốn tạo một sự kiện có tên "Họp" vào sáng mai.
- Tôi cần trích xuất thông tin về thời gian từ câu hỏi của người dùng.
- Action: "extract_datetime"
- Action Input: {{{{"text": "Tạo lịch họp vào sáng mai", "intent": "create_normal_event"}}}}
- {{{{'is_recurring': False, 'incorrect_datetime': False, 'title': 'Họp', 'datetime_ranges': [{{'start_datetime': '2025-05-21 00:00:00', 'end_datetime': '2025-05-21 12:00:00'}}], 'location': '', 'intent': 'create_normal_event'}}}}
- Ngôn ngữ của người dùng là tiếng Việt. Dựa vào kết quả của công cụ extract_datetime, tôi đã có các thông tin. Bây giờ tôi sẽ sử dụng công cụ create_normal_event để tạo sự kiện.
- Action: create_normal_event
- Action Input: {{{{'is_recurring': False, 'incorrect_datetime': False, 'title': 'họp', 'datetime_ranges': [{{'start_datetime': '2025-05-21 00:00:00', 'end_datetime': '2025-05-21 12:00:00'}}], 'location': '', 'intent': 'create_normal_event'}}}}
Nếu đã đủ thông tin, bạn có thể trả về kết quả/trạng thái cuối cùng:

Final Answer: <kết quả/trạng thái>
Bắt đầu!

Question: {input}
Thought:{agent_scratchpad}""",
)

# Tạo memory để lưu trữ lịch sử trò chuyện

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=5, return_messages=True
)

# Tạo agent_executor với memory đã cấu hình
agent_executor = create_react_agent_executor(
    tools=tools,
    prompt_template=prompt_template,
    memory=memory,
)
# # Create the ReAct agent with memory - Commented for reference
# agent = create_react_agent(
#     llm=llm,
#     tools=tools,
#     prompt=prompt_template
# )
# # Create an agent executor
# agent_executor = AgentExecutor.from_agent_and_tools(
#     agent=agent,
#     tools=tools,
#     verbose=True,
#     handle_parsing_errors=True, # Giúp xử lý lỗi parsing output của LLM tốt hơn
#     max_iterations=5, # Giới hạn số lần lặp để tránh vòng lặp vô hạn
#     memory=memory
# )

# Test run
if __name__ == "__main__":
    # Thực hiện một chuỗi các truy vấn để thử nghiệm khả năng nhớ của agent
    queries = [
        # "Ngày 30/05/2025 rảnh lúc nào",
        # "Xin chào, tôi tên là Thắng",
        "Tạo lịch h",
        "Lúc 9h sáng mai",
        # "Tôi tên gì và vừa làm gì?"
        # "Bạn nhớ lúc nãy tôi hỏi gì không?",
        # "Xóa toàn bộ lịch trong năm 2025"
    ]

    # Chạy từng truy vấn theo thứ tự và giữ nguyên bộ nhớ giữa các lần gọi
    for i, query in enumerate(queries):
        print(f"\n--- Truy vấn {i+1}: {query} ---\n")
        result = agent_executor.invoke({"input": query})
        print("\nFinal Answer:", result.get("output"))
        print("\n" + "-" * 50)
# import gradio as gr

# async def chat_with_bot(messages):
#     user_msg = messages[-1]["content"]
#     reply = agent_executor.invoke({"input": user_msg}).get("output")
#     messages.append({"role": "assistant", "content": reply})
#     return messages

# gr.ChatInterface(fn=chat_with_bot, type="messages").launch()
