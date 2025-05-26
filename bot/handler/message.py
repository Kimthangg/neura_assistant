import json

from bot.agent_calendar import *
from features import *


def full_flow(action_input):
    # Chuyển đổi action_input từ JSON string sang dict
    func_args = json.loads(action_input)
    # Lấy các tham số từ action_input
    user_message = func_args.get("text")
    intent = func_args.get("intent").strip()
    print("intent", intent)
    print("user_message", user_message)
    if not intent or intent == "normal_message":
        # extraction = {'content':get_llm(user_message)}
        extraction = {"intent": "normal_message"}

    # Create event
    elif intent == "create_normal_event":
        extraction = create_event_extraction(user_message)

    # get event
    elif intent in ["get_first_calendar", "get_freetime", "get_multi_calendar"]:
        # Extract datetime from text
        extraction = get_event_extraction(user_message)
    # Update event
    elif intent == "update_event":
        extraction = update_event_extraction(user_message)

    # Delete event
    elif intent == "delete_event":
        extraction = delete_event_extraction(user_message)
    print("intent", intent)
    print("extraction", extraction)
    # Add intent to extraction dictionary and return
    extraction["intent"] = intent
    if intent in ["create_normal_event", "update_event", "delete_event"]:
        with open("last_parameter.json", "w", encoding="utf-8") as f:
            json.dump(extraction, f, ensure_ascii=False, indent=2)
            print("Đã lưu extraction vào last_parameter.json")
    return extraction


# def call_api(event):
#     print("Đang gọi api")
#     try:
#         if event.get("intent") == "create_normal_event":
#             event = create_event_api(event)
#         elif event.get("intent") == "get_first_calendar":
#             event = get_first_calendar_api(event)
#         elif event.get("intent") == "get_freetime":
#             event = get_free_time_api(event)
#         elif event.get("intent") == "get_multi_calendar":
#             event = get_multi_calendar_api(event)
#         elif event.get("intent") == "update_event":
#             event = update_event_api(event)
#         elif event.get("intent") == "delete_event":
#             event = delete_event_api(event)
#         else:
#             event = {"error": "Đã xảy ra lỗi khi gọi API"}
#         print("event", event)
#         return event
#     except Exception as e:
#         print("Lỗi khi gọi API:", e)
#         return {"error": "Đã xảy ra lỗi khi gọi API"}
