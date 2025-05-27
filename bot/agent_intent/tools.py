from services.llm.llm_config import LLM
from .prompt import *

intent_model = LLM(supervisor_system_message, tool_supervisor, temperature=0.0)
