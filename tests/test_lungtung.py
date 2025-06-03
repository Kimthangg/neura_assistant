import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

# from bot.agent_calendar import *
# from features import *
# data = '{"title_old": "đi chơi", "title_new": "học nhóm", "location_old": "trường", "location_new": "trường", "datetime_ranges": [{"start_datetime": "2025-05-27 08:00:00", "end_datetime": "2025-05-27 08:00:01", "start_new": "2025-05-27 08:00:00", "end_new": "2025-05-27 08:00:00"}], "incorrect_datetime": False}'
# print(update_event_api(data))
from features.gmail_features.summarize_emails import summarize_emails_api


args = {'sender': '', 'subject': '', 'keyword': '', 'start_date': '2025-05-31', 'end_date': '2025-06-01', 'incorrect_datetime': False}
print(summarize_emails_api(args))