from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from features import calendar_features_map

# Openrouter
# API_KEY = "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"
# API_BASE = "https://openrouter.ai/api/v1"

# AI Studio
API_KEY = "AIzaSyAzfZhskIaC2WcBP29QDloc-p71ZbwGUko"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_NAME = "gemini-2.0-flash"
llm = ChatOpenAI(
    api_key=API_KEY,
    openai_api_base=API_BASE,
    model=MODEL_NAME,
    # function_call="auto",
)

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
# from bot import extract_datetime_get_event
# from langchain.tools import StructuredTool


# extract_datetime_tool = StructuredTool.from_function(
#     name="extract_datetime",
#     description="Extract datetime ranges from text",
#     func=extract_datetime_get_event,
#     args_schema=None,

# )
# # Add the datetime extractor tool to the list of tools
# tools.append(extract_datetime_tool)
# Lấy tên các công cụ
tool_names = [tool.name for tool in tools]
prompt_template = PromptTemplate(
    input_variables=["agent_scratchpad", "input"],
    template="""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""",
)
# Create the ReAct agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)

# Create an agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

# Test run
if __name__ == "__main__":
    query = "Lấy sự kiện vào sáng mai"  # Example query
    result = agent_executor.invoke({"input": query})
    print("\nFinal Answer:", result.get("output"))
