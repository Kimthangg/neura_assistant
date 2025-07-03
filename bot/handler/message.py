import json
from bot import *
from services.llm.llm_config import *
from features import *

def full_flow(action_input):
    # Chuyển đổi action_input từ JSON string sang dict
    func_args = json.loads(action_input)
    # Lấy các tham số từ action_input
    user_message = func_args.get("text")
    intent = func_args.get("intent").strip()
    print("intent", intent)
    print("user_message", user_message)
    # ============CALENDAR================
    if not intent or intent == "normal_message":
        # extraction = {'content':get_llm(user_message)}
        extraction = {"intent": "normal_message"}
    # Create event
    elif intent == "create_normal_event":
        extraction = LLM(system_prompt_create_event, tool_create_event, temperature=0.1)(user_message)
    # get event
    elif intent in ["get_first_calendar", "get_freetime", "get_multi_calendar"]:
        # Extract datetime from text
        extraction = LLM(system_prompt_get_event, tool_get_event, temperature=0.1)(user_message)
    # Update event
    elif intent == "update_event":
        extraction = LLM(system_prompt_update_event, tool_update_event, temperature=0.1)(user_message)
    # Delete event
    elif intent == "delete_event":
        extraction = LLM(system_prompt_delete_event, tool_delete_event, temperature=0.1)(user_message)
    # ============GMAIL================
    elif intent == "summarize_emails":
        extraction = LLM(system_prompt_summarize_emails, tool_summarize_emails, temperature=0.1)(user_message)
    print("intent", intent)
    print("extraction", extraction)
    # Add intent to extraction dictionary and return
    extraction["intent"] = intent
    if intent in ["create_normal_event", "update_event", "delete_event"]:
        with open("last_parameter.json", "w", encoding="utf-8") as f:
            json.dump(extraction, f, ensure_ascii=False, indent=2)
            print("Đã lưu extraction vào last_parameter.json")
    return extraction
