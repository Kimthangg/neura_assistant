import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

from config.calendar import xac_thuc_calendar

service, CALENDAR_ID = xac_thuc_calendar()

# Lấy danh sách sự kiện
events = service.events().list(calendarId=CALENDAR_ID, maxResults=2500).execute()

# Lặp qua tất cả sự kiện và xóa chúng
if "items" in events:
    for event in events["items"]:
        event_id = event["id"]
        try:
            service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
            print(f"Event {event_id} deleted.")
        except Exception as e:
            print(f"An error occurred while deleting event {event_id}: {e}")
else:
    print("No events found in the calendar.")
