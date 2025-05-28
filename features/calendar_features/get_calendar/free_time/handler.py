from config.calendar import xac_thuc_calendar
from utils import *


def get_freetime(busy_periods: list, time_min: str, time_max: str) -> list:
    """
    Calculates free time slots based on busy periods.

    Parameters:
    busy_periods (list): A list of dictionaries, each containing 'start' and 'end' keys with ISO 8601 datetime strings.
    time_min (str): The minimum time boundary as an ISO 8601 datetime string.
    time_max (str): The maximum time boundary as an ISO 8601 datetime string.

    Returns:
    list: A list of dictionaries representing free time slots, each with 'start' and 'end' keys as ISO 8601 datetime strings.
    """
    dt_min = datetime.fromisoformat(time_min)
    dt_max = datetime.fromisoformat(time_max)
    free_times = []
    last_free_time = dt_min
    for busy_period in busy_periods:
        start = datetime.fromisoformat(busy_period["start"])
        end = datetime.fromisoformat(busy_period["end"])
        if start > last_free_time:
            free_times.append(
                {"start": last_free_time.isoformat(), "end": start.isoformat()}
            )
        last_free_time = end
    if last_free_time < dt_max:
        free_times.append(
            {"start": last_free_time.isoformat(), "end": dt_max.isoformat()}
        )
    return free_times


def get_free_time_api(function_args, timeZone: str = "Asia/Ho_Chi_Minh") -> dict:
    function_args = parse_to_dict(function_args)
    # Tạo dịch vụ Google Calendar API
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
    service, CALENDAR_ID = xac_thuc_calendar()
    body = {
        "timeMin": st_datetime_str,
        "timeMax": ed_datetime_str,
        "timeZone": timeZone,
        "items": [{"id": CALENDAR_ID}],
    }

    freebusy = service.freebusy().query(body=body).execute()
    busy_periods = freebusy.get("calendars", {}).get(CALENDAR_ID, {}).get("busy", [])
    # print("freebusy",freebusy)
    # print("busy",busy_periods)
    free_times = get_freetime(busy_periods, st_datetime_str, ed_datetime_str)

    if len(free_times):
        return free_times

    return {"error": message_no_get_calendar}
