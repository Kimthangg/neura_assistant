from datetime import datetime, timedelta

from config.calendar import xac_thuc_calendar
from utils import *

service, calendar_id = xac_thuc_calendar()


def delete_calendar(event_id, event):
    """
    Xóa một sự kiện từ Google Calendar.
    Args:
        event_id (str): ID của sự kiện cần xóa.
        event (dict): Thông tin của sự kiện, được sử dụng để trả về thông tin sau khi xóa.
    Returns:
        dict: Thông tin của sự kiện đã bị xóa, được trả về từ hàm get_info_event.
    Raises:
        Exception: Nếu có lỗi xảy ra trong quá trình xóa sự kiện, lỗi sẽ được in ra màn hình.
    """

    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return (f"Đã xóa sự kiện {event['summary']} thành công!")
    except Exception as e:
        return (f"Lỗi khi xóa sự kiện {event['summary']}: {e}")

    # return get_info_event(event)


def delete_event_api(function_args, timeZone: str = "Asia/Ho_Chi_Minh") -> dict:
    """
    Xóa sự kiện từ Google Calendar dựa trên thông tin thời gian được cung cấp.
    Hàm này tìm kiếm các sự kiện trong khoảng thời gian được chỉ định và thực hiện xóa:
    - Nếu tìm thấy một sự kiện, xóa sự kiện đó
    - Nếu tìm thấy nhiều sự kiện, trả về danh sách các sự kiện để người dùng có thể chọn
    Args:
        function_args (dict): Từ điển chứa thông tin về sự kiện cần xóa, bao gồm:
            - datetime_ranges: Danh sách các khoảng thời gian
                - start_datetime: Thời gian bắt đầu (định dạng: "%Y-%m-%d %H:%M:%S")
                - end_datetime: Thời gian kết thúc (định dạng: "%Y-%m-%d %H:%M:%S")
            - incorrect_datetime: Cờ đánh dấu nếu định dạng thời gian không hợp lệ
        timeZone (str, optional): Múi giờ sử dụng. Mặc định là "Asia/Ho_Chi_Minh".
    Returns:
        dict: Kết quả của việc xóa sự kiện:
            - Thông báo lỗi nếu thời gian không hợp lệ
            - Thông báo không tìm thấy sự kiện nếu không có sự kiện nào trong khoảng thời gian
            - Kết quả của việc xóa sự kiện nếu chỉ có một sự kiện
            - Danh sách các sự kiện nếu có nhiều sự kiện trong khoảng thời gian
    """
    function_args = parse_to_dict(function_args)
    print("function_args", function_args)
    if function_args.get("incorrect_datetime"):
        return invalid_time
    try:
        if (
            function_args["datetime_ranges"][0]["start_datetime"]
            == function_args["datetime_ranges"][0]["end_datetime"]
        ):
            print("start_datetime == end_datetime")
            temp = datetime.strptime(
                function_args["datetime_ranges"][0]["end_datetime"], "%Y-%m-%d %H:%M:%S"
            ) + timedelta(seconds=1)
            function_args["datetime_ranges"][0]["end_datetime"] = temp.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        st_datetime_str = convert_to_iso_format(
            function_args["datetime_ranges"][0]["start_datetime"]
        )
        ed_datetime_str = convert_to_iso_format(
            function_args["datetime_ranges"][0]["end_datetime"]
        )
        print("st_datetime_str", st_datetime_str)
        print("ed_datetime_str", ed_datetime_str)
    except Exception as e:
        print(e)
    # Lấy danh sách sự kiện trong khoảng thời gian
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=st_datetime_str,
            timeMax=ed_datetime_str,
            singleEvents=True,
            orderBy="startTime",  # Nếu muốn sắp xếp theo thời gian bắt đầu thì phải singleEvents=True
            timeZone=timeZone,
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
        return {"error": message_no_get_calendar}

    if len(events) == 1:
        # Cập nhật sự kiện nếu chỉ có 1 sự kiện
        event_id = events[0]["id"]
        event = events[0]
        return delete_calendar(event_id, event)

    # Nếu có nhiều hơn 1 sự kiện, trả về danh sách sự kiện
    event_list = []
    for event in events:
        event_list.append(delete_calendar(event["id"], event))
    return event_list
