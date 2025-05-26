from config.calendar import xac_thuc_calendar
from utils import *
from rapidfuzz import fuzz

def update_event_api(function_args, timeZone: str = "Asia/Ho_Chi_Minh") -> dict:
    """
    function_args gồm:
      - title_old, location_old,
      - title_new, location_new,
      - start_datetime, end_datetime,
      - start_new, end_new
    """
    args = parse_to_dict(function_args)
    service, calendar_id = xac_thuc_calendar()

    # 1. Chuyển thời gian sang ISO
    try:
        st_old = convert_to_iso_format(args['datetime_ranges'][0]['start_datetime'])
        ed_old = convert_to_iso_format(args['datetime_ranges'][0]['end_datetime'])
        st_new = convert_to_iso_format(args['datetime_ranges'][0]['start_new'])
        ed_new = convert_to_iso_format(args['datetime_ranges'][0]['end_new'])
    except Exception as e:
        return {"error": f"Không parse được thời gian: {e}"}
    page_token = None
    event_list = []
    while not event_list:
        # 2. Lấy events trong khoảng cũ
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=st_old,
            timeMax=ed_old,
            singleEvents=True,
            orderBy='startTime',
            timeZone=timeZone,
        ).execute()
        events = events_result.get('items', [])
        # Nếu không có sự kiện, lấy pageToken để kiểm tra trang tiếp theo
        page_token = events_result.get("nextPageToken")
        if not page_token:
            break  # Không còn trang nào để tìm
    if not events:
        return {"error": message_no_get_calendar}

    # 3. Nếu chỉ 1 sự kiện thì chọn luôn
    if len(events) == 1:
        target = events[0]
    else:
        # 3.a. Lọc bằng title_old nếu có
        if args.get('title_old'):
            filtered = [
                ev for ev, score in
                ((ev, fuzz.partial_ratio(args['title_old'], ev.get('summary', ''))) for ev in events)
                if score >= 80
            ]
            if filtered:
                events = filtered

        # 3.b. Nếu vẫn >1 và có location_old thì lọc tiếp
        if len(events) > 1 and args.get('location_old'):
            filtered_loc = [
                ev for ev, score in
                ((ev, fuzz.partial_ratio(args['location_old'], ev.get('location', ''))) for ev in events)
                if score >= 80
            ]
            if filtered_loc:
                events = filtered_loc

        # 3.c. Kết quả cuối cùng
        if len(events) == 1:
            target = events[0]
        else:
            # trả về danh sách để user chọn
            return [
                {
                    'id': ev['id'],
                    'summary': ev.get('summary', ''),
                    'location': ev.get('location', ''),
                    'start': ev.get('start', {}).get('dateTime', ''),
                    'end': ev.get('end', {}).get('dateTime', '')
                }
                for ev in events
            ]

    # 4. Cập nhật sự kiện
    if args.get('title_new') is not None:
        target['summary'] = args['title_new'].capitalize() #in hoa vào đầu chữ
    if args.get('location_new') is not None:
        target['location'] = args['location_new'].capitalize()
    target['start'] = {'dateTime': st_new, 'timeZone': timeZone}
    target['end']   = {'dateTime': ed_new, 'timeZone': timeZone}

    updated = service.events().update(
        calendarId=calendar_id,
        eventId=target['id'],
        body=target,
    ).execute()

    return updated
