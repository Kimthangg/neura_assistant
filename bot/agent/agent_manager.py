from langchain.agents import Tool
from langchain.prompts import PromptTemplate

from .agent_calendar import agent_calendar_executor_func
from .agent_gmail import agent_gmail_executor_func
from services.llm.llm_config import create_react_agent_executor
tools = []
tools.append(
Tool(
    name="agent_calendar",
    func=agent_calendar_executor_func,
    description="""Xử lý các câu truy vấn liên quan đến lịch, bao gồm tạo, xem, cập nhật, xóa sự kiện lịch và 
    tìm thời gian rảnh, tìm lịch đầu tiên vào khoảng thời gian nào đó, lấy được thông tin nhiều lịch trong một khoảng thời gian""",
)
)
tools.append(
    Tool(
    name="agent_gmail",
    func=agent_gmail_executor_func,
    description="""Xử lý các câu truy vấn liên quan đến Gmail, bao gồm:
    - Tóm tắt email trong khoảng thời gian đã cho
    - Dựa vào bản tóm tắt có thể lấy được các thông tin về ngày tháng, địa điểm để tạo lịch dưới sự đồng ý của người dùng
    - Cảnh báo các email có deadline gần đến hạn từ bản tóm tắt
    
    - Tự động phân loại và gắn nhãn mail (công việc, cá nhân, quan trọng, gần đến hạn)
    - Trợ lý tìm kiếm email thông minh với nội dung cụ thể""",
))

tool_names = [tool.name for tool in tools]
prompt_template = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "chat_history", "tools"],
    template="""Bạn là một trợ lý AI thông minh tên Neura, có khả năng phân tích ý định của người dùng và điều phối các agent chuyên biệt.

    Nhiệm vụ chính của bạn:
    1. Phân tích ý định và nhu cầu của người dùng từ câu hỏi
    2. Xác định agent phù hợp nhất để xử lý yêu cầu
    3. Chuyển đổi câu hỏi thành định dạng phù hợp cho agent được chọn
    4. Điều phối và theo dõi quá trình xử lý:
    - Đưa ra câu trả lời cuối cùng cho người dùng y nguyên agent calendar hoặc agent gmail trả về, không sửa đổi.
    - Nếu agent calendar hoặc agent gmail cần xác nhận thông tin từ người dùng, hãy hỏi lại người dùng(đưa ra Final Answer y nguyên) để lấy thông tin chính xác hơn không được tự ý quyết định.
    Bạn có quyền truy cập vào các công cụ sau:
    {tools}
    
    Lịch sử cuộc trò chuyện:
    {chat_history}
    
    Quy trình xử lý:
    - Nếu liên quan đến lịch (tạo, xem, sửa, xóa sự kiện, tìm thời gian rảnh): sử dụng agent_calendar
    - Nếu liên quan đến email (tóm tắt, phân loại, tìm kiếm): sử dụng agent_gmail
    - Nếu là câu hỏi chung không liên quan đến lịch hoặc email: hãy trả lời bằng ngôn ngữ của người dùng (tiếng Việt hoặc tiếng Anh) một cách tự nhiên và hữu ích
    - Nếu không rõ ý định, hãy hỏi lại người dùng để lấy thông tin chính xác hơn
    - Nếu có yêu cầu phức tạp liên quan đến cả hai: chia nhỏ và xử lý tuần tự

    Hãy sử dụng định dạng sau để trả lời nếu sử dụng tool agent_calendar hoặc agent_gmail:
    Question: câu hỏi mà bạn phải trả lời
    Thought: phân tích ý định người dùng và xác định agent phù hợp
    Action: hành động cần thực hiện, phải là một trong [{tool_names}]
    Action Input: câu truy vấn được chuyển đổi cho agent được chọn
    Observation: kết quả từ agent giữ nguyên và đưa ra y nguyên không sửa đổi, bao gồm cả các trường rỗng thông tin.
    ... (quá trình Thought/Action/Action Input/Observation KHÔNG LẶP LẠI NHIỀU LẦN, chỉ cần thực hiện một lần duy nhất)
    Nếu agent_calendar hoặc agent_gmail cần xác nhận thông tin từ người dùng, hãy hỏi lại người dùng để lấy thông tin chính xác hơn.
    Nếu đã đủ thông tin hoặc gặp lỗi, bạn có thể trả về kết quả/trạng thái cuối cùng:
    Final Answer: Đưa ra câu trả lời cuối cùng cho người dùng dựa trên kết quả từ agent

    Ví dụ câu hỏi về lịch:
        Input: "Tạo lịch họp vào sáng mai lúc 9h"
        Thought: Người dùng muốn tạo một sự kiện lịch vào sáng mai lúc 9h.
        Tôi sẽ sử dụng agent_calendar để xử lý yêu cầu này.
        Action: agent_calendar
        Action Input: {{Câu truy vấn của người dùng là: "Tạo lịch họp vào sáng mai lúc 9h"}}
        Observation: Bạn muốn tạo một sự kiện có tên "Họp" vào sáng mai (2025-05-26) từ 09:00 đến 09:00. Địa điểm không được cung cấp. Bạn có muốn tiếp tục không?
        Final Answer: Bạn muốn tạo một sự kiện có tên "Họp" vào sáng mai (2025-05-26) từ 09:00 đến 09:00. Địa điểm không được cung cấp. Bạn có muốn tiếp tục không?
        
        Kết thúc quá trình đưa Final Answer để hỏi người dùng, nếu người dùng xác nhận thông tin:
        Input 2: Đúng rồi
        Thought 2: Người dùng đã xác nhận thông tin "Tạo lịch họp vào sáng mai lúc 9h". Tôi sẽ tiến hành tạo sự kiện lịch.
        Action 2: agent_calendar
        Action Input 2: Người dùng đã xác nhận thông tin "Tạo lịch họp vào sáng mai lúc 9h". Tôi sẽ tiến hành tạo sự kiện lịch.
        Observation: Sự kiện lịch đã được tạo thành công vào sáng mai (2025-05-26) từ 09:00 đến 09:00. Địa điểm không được cung cấp
        Final Answer 2: Sự kiện lịch đã được tạo thành công vào sáng mai (2025-05-26) từ 09:00 đến 09:00. Địa điểm không được cung cấp
    
    Hãy sử dụng định dạng sau để trả lời các câu hỏi không liên quan đến lịch hoặc email:
    Input: câu hỏi của người dùng
    Final Answer: câu trả lời tự nhiên và hữu ích cho người dùng
    
    Bắt đầu:
    Question: {input}
    {agent_scratchpad}"""
)
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory


from utils import convert_list_to_messages
def agent_manager_executor_func(query, history_chat=None):
    """
    Hàm thực thi agent_executor với truy vấn đầu vào và thêm lịch sử chat nếu có.

    Parameters:
        query (str): Truy vấn đầu vào từ người dùng.
        history_chat (list): Lịch sử trò chuyện dạng list (dicts hoặc messages).

    Returns:
        str: Kết quả từ agent_executor hoặc thông báo lỗi.
    """
    # print("Đang load lịch sử chat:", history_chat)
    memory_manager = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=3,  # Số lượng tin nhắn trong lịch sử chat
    )
    if history_chat:
        # Convert lịch sử về messages
        messages = convert_list_to_messages(history_chat)
        # Nạp lại vào memory
        memory_manager.chat_memory.messages = messages
    else:
        print("Không có lịch sử chat để nạp vào memory.")
    # print("\nLịch sử chat đã được nạp vào memory:", memory_manager.chat_memory.messages)
    # Tạo agent_executor với memory đã cấu hình
    agent_executor = create_react_agent_executor(
        tools=tools,
        memory=memory_manager,
        prompt_template=prompt_template,
        option_api=2
    )
    print("\nAgent Manager đang xử lý...")
    result = agent_executor.invoke({"input": query})
    return result.get("output", "Lỗi trong quá trình thực thi!")