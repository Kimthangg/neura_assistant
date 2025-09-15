from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

# from config.environment import API_KEY, API_BASE, MODEL_NAME, API_KEY_2, API_KEY_3, API_KEY_4
import random
import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Lấy các biến ra
API_KEY = os.getenv("API_KEY")
API_BASE = os.getenv("API_BASE")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY_2 = os.getenv("API_KEY_2")
API_KEY_3 = os.getenv("API_KEY_3")
API_KEY_4 = os.getenv("API_KEY_4")

class LLM:
    _api_keys = {
        1: API_KEY,
        2: API_KEY_2,
        3: API_KEY_3,
        4: API_KEY_4,
    }
    def __init__(self, system_message: str, tool: dict, model_name: str = MODEL_NAME, temperature: float = 0.0):
        """
        Initializes the LLM class with a specified system message, tool, model name, and temperature.

        Parameters:
        system_message (str): The system message to be used by the language model.
        tool (dict): A dictionary representing the tool to be bound to the model.
        model_name (str): The name of the model to be used. Defaults to MODEL_NAME.
        temperature (float): The temperature setting for the model, affecting randomness. Defaults to 0.
        """
        api_num = random.choice(list(LLM._api_keys.keys()))
        print(f"Using API key number: {api_num} for model {model_name}")
        api_key = LLM._api_keys[api_num]
        self.model = ChatOpenAI(
            api_key=api_key,
            openai_api_base=API_BASE,
            model=MODEL_NAME,
            temperature=temperature,
            # streaming=True,
        )
        # , tool_choice=tool["name"]
        if tool is not None:
            self.model = self.model.bind_tools([tool])
        self.system_message = system_message

    def __call__(self, user_message: str):
        """
        Invokes the language model with a user message and returns the function name and arguments if any tool calls are made.

        Parameters:
        user_message (str): The message from the user to be processed by the language model.

        Returns:
        tuple: A tuple containing the function name and arguments if a tool call is made, otherwise (None, {}).
        """
        response = self.model.invoke(
            [
                ("system", self.system_message),
                ("user", user_message),
            ]
        )
        # print(f"response = {response}")
        # print(f"model = {self.model}")
        # print(f"system message = {self.system_message}")
        if len(response.tool_calls):  # need to get calendar info
            response.tool_calls[0].get("name", "")
            function_args = response.tool_calls[0].get("args")
            response.usage_metadata.get("total_tokens", -1)
            # print(f"{function_name} {function_args} {token_used}")
            # return function_name, function_args
            return function_args

        return {}

from langchain_core.prompts import PromptTemplate
def llm_summarize(model_name: str = MODEL_NAME, temperature: float = 0.0, option_api: int = 4):
    """
    Tạo một chain xử lý để tóm tắt nội dung email sử dụng mô hình ngôn ngữ lớn.
    Hàm này khởi tạo một ChatOpenAI instance và kết hợp với một prompt template được thiết kế 
    để tóm tắt danh sách các email. Prompt yêu cầu mô hình trích xuất thông tin quan trọng 
    như subject, ngày gửi, người gửi và các thông tin liên quan đến lịch (ngày tháng, địa điểm).
    Parameters:
        model_name (str, optional): Tên của mô hình OpenAI được sử dụng. 
                                   Mặc định là giá trị của MODEL_NAME.
        temperature (float, optional): Tham số nhiệt độ điều chỉnh độ ngẫu nhiên 
                                      của đầu ra. Mặc định là 0.0.
    Returns:
        Chain: Một chain xử lý kết hợp prompt template và mô hình LLM để tóm tắt email.
    """
    llm = ChatOpenAI(
        api_key=API_KEY_4 if option_api == 4
                        else API_KEY_2 if option_api == 2
                        else API_KEY_3,
        openai_api_base=API_BASE,
        model=model_name,
        temperature=temperature,
        max_tokens = 2000,  
    )
    prompt_template = """Bạn là một trợ lý ảo thông minh có khả năng tóm tắt nội dung email. Bạn sẽ nhận vào một danh sách các email và trả về nội dung tóm tắt của chúng kèm các thông tin về subject cũng như ngày gửi, người gửi.
    Nếu chúng có các thông tin ngày tháng, địa điểm(các nội dung có thể tạo lịch) thì đưa ra các thông tin đó cho người dùng biết
    Dưới đây là danh sách các email:
    {mails}
    Bạn cần tóm tắt nội dung của các email này và trả về một danh sách các câu tóm tắt để người dùng có thể hiểu nhanh nội dung của chúng. Mỗi câu tóm tắt nên ngắn gọn và súc tích, chỉ bao gồm các thông tin quan trọng nhất.
    Nếu có các thông tin về ngày tháng, địa điểm trong nội dung email thì hãy đưa ra các thông tin đó cho người dùng biết
    Trả về dưới dạng JSON(luôn luôn có trường id).
    """
    prompt = PromptTemplate(
        input_variables=["mails"],
        template=prompt_template
    ) 
    return prompt | llm

def create_react_agent_executor(
    prompt_template,
    tools,
    memory=None,
    model_name: str = MODEL_NAME,
    temperature: float = 0.0,
    option_api = 1,  # 1: API_KEY, 2: API_KEY_2, 3: API_KEY_3
):
    """
    Tạo một AgentExecutor với ReAct agent.

    Parameters:
        prompt_template: Template prompt cho agent
        tools: Danh sách các tools cho agent
        memory (BaseChatMemory, optional): Đối tượng memory để lưu trữ lịch sử trò chuyện. Mặc định là None.
        model_name (str, optional): Tên model. Mặc định là MODEL_NAME.
        temperature (float, optional): Độ ngẫu nhiên. Mặc định là 0.0.

    Returns:
        AgentExecutor: Đối tượng AgentExecutor đã được cấu hình
    """
    print("Option API:", option_api)
    # Tạo LLM
    llm = ChatOpenAI(
        api_key=API_KEY if option_api == 1 else API_KEY_2,
        openai_api_base=API_BASE,
        model=model_name,
        temperature=temperature,
    )
    # print("\nLịch sử chat đã được nạp vào memory:", memory.chat_memory.messages)
    
    # Tạo ReAct agent
    agent = create_react_agent(llm, tools, prompt_template)


    # Tạo và trả về AgentExecutor
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,  # Giúp xử lý lỗi parsing output của LLM tốt hơn
        max_iterations=6,  # Giới hạn số lần lặp để tránh vòng lặp vô hạn
        memory=memory,  # Thêm memory nếu được cung cấp
        # TimeoutError = 20, # Thời gian chờ tối đa cho mỗi lần gọi tool
    )
