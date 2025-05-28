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

from features.gmail_features import system_prompt_summarize_emails,tool_summarize_emails
from services.llm.llm_config import LLM

prompt = "Tóm tắt giúp tôi các email từ ngày 08/5 đến 10/5"
result = LLM(system_prompt_summarize_emails, tool_summarize_emails, temperature=0.1)(prompt)
print(result)
# print(get_context_mail_api(result))