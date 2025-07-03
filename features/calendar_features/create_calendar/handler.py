from config.auth_gg import xac_thuc_calendar
from utils import *
from datetime import datetime
now = datetime.now().replace(microsecond=0)
def create_event_api(func_data, timeZone: str = "Asia/Ho_Chi_Minh"):
    """
    Tạo sự kiện mới trên Google Calendar thông qua API.

    Args:
        func_data: Dữ liệu sự kiện được truyền vào, bao gồm các trường:
            - title (str): Tiêu đề của sự kiện
            - location (str): Địa điểm tổ chức sự kiện
            - datetime_ranges (list): Danh sách các khoảng thời gian, chứa:
                - start_datetime (str): Thời gian bắt đầu định dạng "YYYY-MM-DD HH:MM:SS"
                - end_datetime (str): Thời gian kết thúc định dạng "YYYY-MM-DD HH:MM:SS"
                - rrules (str, optional): Quy tắc lặp lại theo định dạng RRULE (Định dạng iCalendar)
            - reminders (dict, optional): Cài đặt nhắc nhở, chứa:
                - overrides (list): Danh sách các cài đặt nhắc nhở tùy chỉnh
        timeZone (str, optional): Múi giờ của sự kiện. Mặc định là "Asia/Ho_Chi_Minh".

    Returns:
        dict: Thông tin sự kiện đã được tạo trên Google Calendar hoặc thông báo lỗi nếu có.
              Trả về {"error": str} nếu xảy ra lỗi trong quá trình tạo sự kiện.

    Note:
        - Hàm sẽ tự động điều chỉnh thời gian kết thúc nếu bằng với thời gian bắt đầu
        - Hỗ trợ tạo sự kiện lặp lại thông qua RRULE
        - Có thể cài đặt nhắc nhở tùy chỉnh hoặc sử dụng cài đặt mặc định
    """
    """"""
    event_data = parse_to_dict(func_data)
    print("event_data", event_data)
    # Kiểm tra thời gian có ở trong quá khứ không, so với thời gian hiện tại
    if datetime.strptime(event_data["datetime_ranges"][0]["start_datetime"], "%Y-%m-%d %H:%M:%S") < now:
        return {"error": "Thời gian bắt đầu sự kiện không được ở trong quá khứ."}
    
    # try:
    #     if event_data['datetime_ranges'][0]['start_datetime'] == event_data['datetime_ranges'][0]['end_datetime']:
    #         print("start_datetime == end_datetime")
    #         temp = datetime.strptime(event_data['datetime_ranges'][0]['end_datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=1)
    #         event_data['datetime_ranges'][0]['end_datetime'] = temp.strftime("%Y-%m-%d %H:%M:%S")
    #     st_datetime_str = convert_to_iso_format(event_data['datetime_ranges'][0]['start_datetime'])
    #     ed_datetime_str = convert_to_iso_format(event_data['datetime_ranges'][0]['end_datetime'])
    #     print("st_datetime_str", st_datetime_str)
    #     print("ed_datetime_str", ed_datetime_str)
    # except Exception as e:
    #     print(e)
    # Tạo sự kiện theo định dạng của Google Calendar API
    event = {
        "summary": event_data["title"],
        "location": event_data["location"],
        "start": {
            "dateTime": convert_to_iso_format(
                event_data["datetime_ranges"][0]["start_datetime"]
            ),
            "timeZone": timeZone,
        },
        "end": {
            "dateTime": convert_to_iso_format(
                event_data["datetime_ranges"][0]["end_datetime"]
            ),
            "timeZone": timeZone,
        },
    }
    # Kiểm tra và thêm phần RRULE nếu có
    if "rrules" in event_data["datetime_ranges"][0]:
        if event_data["datetime_ranges"][0]["rrules"] != "":
            if "RRULE:" in event_data["datetime_ranges"][0]["rrules"]:
                # Thêm RRULE vào trong phần recurrence
                event["recurrence"] = [
                    event_data["datetime_ranges"][0][
                        "rrules"
                    ]  # Thêm RRULE vào trong phần recurrence
                ]
            else:
                # Nếu không có "RRULE:" thì thêm vào trong phần rrule
                event["recurrence"] = [
                    f"RRULE:{event_data['datetime_ranges'][0]['rrules']}"
                ]
    # Thêm reminders nếu có
    if "reminders" in event_data:
        try: 
            if event_data["reminders"]["overrides"] != []:
                event["reminders"] = {
                    "useDefault": False,
                    "overrides": event_data["reminders"]["overrides"],
                }
            else:
                event["reminders"] = {"useDefault": True}
        except KeyError:
            event["reminders"] = {"useDefault": True}
    print(event)
    # Tạo đối tượng dịch vụ Google Calendar API
    service, CALENDAR_ID = xac_thuc_calendar()
    try:
        # Kiểm tra xem sự kiện đã tồn tại hay chưa
        created_event = (
            service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        )
        print(f"Sự kiện đã được tạo: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"Lỗi khi kiểm tra sự kiện: {e}")
        return {"error": str(e)}
    return event
