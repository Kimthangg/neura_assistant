from config.calendar import xac_thuc_calendar
from utils import *

def get_multi_calendar_api(function_args, timeZone: str = "Asia/Ho_Chi_Minh") -> dict:
    # Tạo dịch vụ Google Calendar API
    function_args = parse_to_dict(function_args)
    service, CALENDAR_ID = xac_thuc_calendar()
    print("function_args", function_args)
    if function_args["incorrect_datetime"]:
        return invalid_time
    try:
        st_datetime_str = convert_to_iso_format(
            function_args["datetime_ranges"][0]["start_datetime"]
        )
        ed_datetime_str = convert_to_iso_format(
            function_args["datetime_ranges"][0]["end_datetime"]
        )
    except Exception as e:
        print(e)
        return "Lỗi 1"

    page_token = None
    event_list = []
    try:
        while True:
            events = (
                service.events()
                .list(
                    calendarId=CALENDAR_ID,
                    eventTypes="default",
                    pageToken=page_token,
                    maxResults=5,
                    timeMin=st_datetime_str,
                    timeMax=ed_datetime_str,
                    singleEvents=True,
                    orderBy="startTime",
                    timeZone=timeZone,
                )
                .execute()
            )

            for event in events["items"]:
                # nếu sự kiện allday thì có trường date, nếu có thời gian thì có trường dateTime
                if "dateTime" in event["start"]:
                    event_list.append(get_info_event(event))  # Lấy thông tin sự kiện

            page_token = events.get("nextPageToken")
            if not page_token:
                break
    except Exception as e:
        print(e)
    if len(event_list):
        return event_list
    return {"error": message_no_get_calendar}
