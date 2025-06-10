from config.auth_gg import xac_thuc_calendar
from utils import *


# from bot import extract_datetime_get_event
def get_first_calendar_api(function_args, timeZone: str = "Asia/Ho_Chi_Minh") -> dict:
    # def get_first_calendar_api(input: str, timeZone:str = "Asia/Ho_Chi_Minh") -> dict:
    # function_args = extract_datetime_get_event(input, "get_first_calendar")
    function_args = parse_to_dict(function_args)
    # Tạo dịch vụ Google Calendar API
    service, CALENDAR_ID = xac_thuc_calendar()
    print("function_args", function_args)
    try:
        if function_args["incorrect_datetime"]:
            return invalid_time
    except Exception as e:
        print(e)
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
        while not event_list:
            events = (
                service.events()
                .list(
                    calendarId=CALENDAR_ID,
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
            # print("events", events)
            # Lấy danh sách sự kiện
            event_items = events.get("items", [])
            if event_items:
                first_event = event_items[0]  # Lấy sự kiện đầu tiên
                event_list.append(
                    {
                        "summary": first_event.get("summary", "Không có tiêu đề"),
                        "start": first_event["start"].get(
                            "dateTime", first_event["start"].get("date")
                        ),
                        "end": first_event["end"].get(
                            "dateTime", first_event["end"].get("date")
                        ),
                        "htmlLink": first_event.get("htmlLink", ""),
                        "location": first_event.get("location", "Không có địa điểm"),
                    }
                )

            # Nếu không có sự kiện, lấy pageToken để kiểm tra trang tiếp theo
            page_token = events.get("nextPageToken")
            if not page_token:
                break  # Không còn trang nào để tìm
    except Exception as e:
        print(e)
        return "Lỗi 2"
    if len(event_list):
        return event_list[0]  ## Trả về sự kiện đầu tiên
    return {"error": message_no_get_calendar}
