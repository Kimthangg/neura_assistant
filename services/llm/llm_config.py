from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

from config.environment import API_KEY, API_BASE, MODEL_NAME, API_KEY_2, API_KEY_3

class LLM:
    def __init__(self, system_message: str, tool: dict, model_name: str = MODEL_NAME, temperature: float = 0.0,):
        """
        Initializes the LLM class with a specified system message, tool, model name, and temperature.

        Parameters:
        system_message (str): The system message to be used by the language model.
        tool (dict): A dictionary representing the tool to be bound to the model.
        model_name (str): The name of the model to be used. Defaults to MODEL_NAME.
        temperature (float): The temperature setting for the model, affecting randomness. Defaults to 0.
        """
        self.model = ChatOpenAI(
            api_key=API_KEY_3,
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


def llm_gen(model_name: str = MODEL_NAME, temperature: float = 0.5):
    """
    Tạo một đối tượng ChatOpenAI dựa trên các thông số được cung cấp.
    Hàm này tạo và cấu hình một đối tượng ChatOpenAI sử dụng các thông số về model, key API và
    các cài đặt khác được định nghĩa trước.
    Parameters:
        model_name (str, optional): Tên của model OpenAI sẽ được sử dụng.
                                   Mặc định là giá trị của hằng số MODEL_NAME.
        temperature (float, optional): Tham số điều chỉnh độ ngẫu nhiên của kết quả sinh ra.
                                      Mặc định là 1.0.
    Returns:
        ChatOpenAI: Một đối tượng ChatOpenAI đã được cấu hình, sẵn sàng để sử dụng.
    """
    return ChatOpenAI(
        api_key=API_KEY_3,
        openai_api_base=API_BASE,
        model=model_name,
        temperature=temperature,
    )

from langchain.memory import ConversationBufferWindowMemory
memory_bw = ConversationBufferWindowMemory(
    memory_key="chat_history", k=3, 
    return_messages=True,
)
def create_react_agent_executor(
    prompt_template,
    tools,
    memory=memory_bw,
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
