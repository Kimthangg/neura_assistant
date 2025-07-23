import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

# from features import *
# from utils import *

# data = {
#     "datetime_ranges": [
#             {
#                 "start_datetime": "2025-04-07 00:00:00",
#                 "end_datetime": "2025-04-07 23:59:59"
#             }
#         ],
#     "incorrect_datetime": False,
#     }
# # print(get_first_calendar_api(data))
# print(get_free_time_api(data))
# # print(get_multi_calendar_api(data))


# from bot.agent_extraction.update_event import extract_datetime_update_event

# prompt = "Lùi sự kiện 'Gặp đối tác' từ 9h xuống 11h."
# # prompt = "Ngày 15/05 tôi có buổi thi trên trường vào lúc 10 giờ sáng hãy tạo lịch."
# # print(agent_validate_create(prompt))
# response = extract_datetime_update_event(prompt)

# print(f"""
#       start_datetime: {response['datetime_ranges'][0]['start_datetime']}
#       end_datetime: {response['datetime_ranges'][0]['end_datetime']}
#       start_new: {response['datetime_ranges'][0]['start_new']}
#       end_new: {response['datetime_ranges'][0]['end_new']}""")

from features.gmail_features import system_prompt_summarize_emails,tool_summarize_emails, summarize_emails_api
from services.llm.llm_config import LLM

# prompt = "Tóm tắt email từ 5/5 đến 9/5"
prompt = "Tóm tắt email gần đây"

result = LLM(system_prompt_summarize_emails, tool_summarize_emails, temperature=0.1)(prompt)
print(result)
# print(summarize_emails_api(result))

# from features.calendar_features import system_prompt_update_event,tool_update_event, update_event_api
# from services.llm.llm_config import LLM

# prompt = "sửa lịch học tiếng anh ngày 7/7 từ 7h đến 10h sang học từ 8h đến 11h"
# result = LLM(system_prompt_update_event, tool_update_event, temperature=0.1)(prompt)
# print(result)
# # print(summarize_emails_api(result))