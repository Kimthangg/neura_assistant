from langchain.agents import Tool
from langchain.memory import ConversationBufferWindowMemory,  MongoDBChatMessageHistory
from langchain.prompts import PromptTemplate
from bot import agent_calendar_executor_func, agent_gmail_executor_func
from features import calendar_features_map
from services.llm.llm_config import create_react_agent_executor, llm_gen
tools = []
tools.append(
Tool(
    name="agent_calendar",
    func=agent_calendar_executor_func,
    description="""Xử lý các câu truy vấn liên quan đến lịch, bao gồm tạo, xem, cập nhật, xóa sự kiện lịch và 
    tìm thời gian rảnh, tìm lịch đầu tiên vào khoảng thời gian nào đó, lấy được thông tin nhiều lịch trong một khoảng thời gian""",
),
Tool(
    name="agent_gmail",
    func=agent_gmail_executor_func,
    description="""Xử lý các câu truy vấn liên quan đến Gmail, bao gồm:
    - Đọc mail có nội dung liên quan đến lịch và tự động tạo sự kiện lịch
    - Tự động phân loại và gắn nhãn mail (công việc, cá nhân, quan trọng, gần đến hạn)
    - Cảnh báo các email có deadline gần đến hạn
    - Trợ lý tìm kiếm email thông minh với nội dung cụ thể""",
)
)

tools.append(
    Tool(
        name="general_qa",
        func=lambda query: general_qa_func(query),
        description="""Trả lời các câu hỏi chung, hội thoại bình thường, tư vấn và giải đáp thắc mắc không liên quan đến lịch hoặc email.
        Bao gồm: câu hỏi về kiến thức tổng quát, tư vấn, trò chuyện thông thường, giải thích khái niệm.""",
    )
)

def general_qa_func(query):
    """
    Hàm xử lý các câu hỏi chung không liên quan đến lịch hoặc email.
    
    Parameters:
        query (str): Câu hỏi từ người dùng.
        
    Returns:
        str: Câu trả lời cho câu hỏi.
    """
    try:
        # Sử dụng LLM để trả lời câu hỏi chung
        response = llm_gen.invoke(f"Hãy trả lời câu hỏi sau một cách hữu ích và chính xác: {query}")
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        return f"Xin lỗi, tôi không thể trả lời câu hỏi này lúc này. Lỗi: {str(e)}"

tool_names = [tool.name for tool in tools]
prompt_template = PromptTemplate(
    input_variables=["input", "intermediate_steps", "agent_scratchpad", "chat_history"],
    template="""Bạn là một trợ lý AI thông minh có khả năng phân tích ý định của người dùng và điều phối các agent chuyên biệt.

    Nhiệm vụ chính của bạn:
    1. Phân tích ý định và nhu cầu của người dùng từ câu hỏi
    2. Xác định agent phù hợp nhất để xử lý yêu cầu
    3. Chuyển đổi câu hỏi thành định dạng phù hợp cho agent được chọn
    4. Điều phối và theo dõi quá trình xử lý

    Bạn có quyền truy cập vào các công cụ sau:
    {tools}

    Quy trình xử lý:
    - Nếu liên quan đến lịch (tạo, xem, sửa, xóa sự kiện, tìm thời gian rảnh): sử dụng agent_calendar
    - Nếu liên quan đến email (đọc, phân loại, tìm kiếm, cảnh báo deadline): sử dụng agent_gmail
    - Nếu có yêu cầu phức tạp liên quan đến cả hai: chia nhỏ và xử lý tuần tự

    Hãy sử dụng định dạng sau để trả lời:

    Question: câu hỏi mà bạn phải trả lời
    Thought: phân tích ý định người dùng và xác định agent phù hợp
    Action: hành động cần thực hiện, phải là một trong [{tool_names}]
    Action Input: câu truy vấn được chuyển đổi cho agent được chọn
    Observation: kết quả từ agent
    ... (quá trình Thought/Action/Action Input/Observation có thể lặp lại N lần)
    Thought: Tôi đã có đủ thông tin để trả lời
    Final Answer: tổng hợp kết quả và đưa ra câu trả lời cuối cùng

    Lịch sử hội thoại:
    {chat_history}

    Question: {input}
    {agent_scratchpad}"""
)

def agent_manager_executor_func(query, history_chat):
    """
    Hàm thực thi agent_executor với truy vấn đầu vào.

    Parameters:
        query (str): Truy vấn đầu vào từ người dùng.

    Returns:
        dict: Kết quả trả về từ agent_executor.
    """
    # Tạo memory để lưu trữ lịch sử trò chuyện
    print("history_chat", history_chat)
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", 
        k=3, 
        return_messages=True,
        history_chat = history_chat
    )

    # Tạo agent_executor với memory đã cấu hình
    agent_executor = create_react_agent_executor(
        tools=tools,
        prompt_template=prompt_template,
        memory=memory,
    )

    # Gọi agent_executor với truy vấn đầu vào
    result = agent_executor.invoke({"input": query})
    # return  result
    # Trả về kết quả
    return result.get("output", "Lỗi trong quá trình thực thi!.")
