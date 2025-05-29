def get_info_event(event) -> dict:
    """
    Trích xuất thông tin từ một sự kiện trong Google Calendar.
    Trả về một từ điển chứa các thông tin cần thiết.
    """
    return {
        "summary": event.get("summary", "Không có tiêu đề"),
        "start": event["start"].get("dateTime", event["start"].get("date")),
        "end": event["end"].get("dateTime", event["end"].get("date")),
        "htmlLink": event.get("htmlLink", ""),
        "location": event.get("location", "Không có địa điểm"),
    }


from datetime import datetime, timedelta
import pytz
def convert_to_iso_format(datetime_str):
    """
    Chuyển đổi một chuỗi thời gian sang định dạng ISO 8601 với múi giờ cố định (+07:00).
    Tham số:
        datetime_str (str): Chuỗi đại diện cho thời gian theo định dạng "YYYY-MM-DD HH:MM:SS".
    Trả về:
        str: Chuỗi thời gian đã được chuyển sang định dạng ISO 8601, ví dụ "YYYY-MM-DDTHH:MM:SS+07:00".
    Ví dụ:
        >>> convert_to_iso_format("2023-08-01 12:30:45")
        '2023-08-01T12:30:45+07:00'
    """
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return dt.isoformat() + "+07:00"  # Thêm múi giờ


import calendar
# Trả về ngày hợp lệ tiếp theo
def get_next_valid_date(day):
    """
    Trả về đối tượng datetime đại diện cho ngày hợp lệ tiếp theo dựa trên ngày đã cho.
    Tham số:
        day (int): Ngày mong muốn (ví dụ, 15). Nếu ngày đã qua trong tháng hiện tại, hàm sẽ tìm ngày hợp lệ cho tháng tiếp theo.
    Trả về:
        datetime: Đối tượng datetime với năm, tháng được xác định dựa trên thời điểm hiện tại và tham số day.
        - Nếu ngày hiện tại đã vượt qua giá trị day, hàm sẽ chuyển sang tháng kế tiếp (và năm mới nếu cần).
        - Trong trường hợp của tháng 2, nếu không phải năm nhuận và giá trị day vượt quá 28, hàm sẽ chuyển sang tháng 3.
        - Nếu giá trị day vượt quá số ngày của tháng (ví dụ: 31 đối với tháng chỉ có 30 ngày), hàm sẽ chọn ngày cuối cùng của tháng đó.
    """

    now = datetime.now()
    year, month = now.year, now.month

    # Nếu ngày đã qua trong tháng hiện tại, chuyển sang tháng tiếp theo
    if now.day > day:
        month += 1
        if month > 12:  # Nếu đang ở tháng 12 thì chuyển sang năm sau
            month = 1
            year += 1

    # Xử lý tháng 2 (kiểm tra năm nhuận)
    if month == 2 and day > 28 and not calendar.isleap(year):
        month = 3

    # Lấy ngày cuối cùng của tháng để tránh lỗi ngày vượt quá số ngày của tháng
    last_day = calendar.monthrange(year, month)[1]
    valid_day = min(day, last_day)

    return datetime(year, month, valid_day)


def get_weekdays_context(timezone: str = "Asia/Ho_Chi_Minh"):
    """
    Hàm get_weekdays_context lấy danh sách các ngày trong tuần của tuần hiện tại và tuần kế tiếp.
    Tham số:
        timezone (str): Múi giờ để xác định thời gian hiện tại. Mặc định là 'Asia/Ho_Chi_Minh'.
    Trả về:
        List[datetime]: Danh sách các đối tượng datetime cho từng ngày trong tuần (từ thứ Hai đến Chủ Nhật)
        của tuần hiện tại và tuần kế tiếp.
    """
    now = datetime.now(pytz.timezone(timezone))
    this_week = now - timedelta(days=now.weekday())
    next_week = this_week + timedelta(days=7)
    # Get all weekdays for last, current and next week
    weekdays = []
    for week_start in [this_week, next_week]:
        for i in range(7):  # Monday (0) to Sunday (6)
            weekdays.append(week_start + timedelta(days=i))
    return weekdays


def get_context_date(timezone: str = "Asia/Ho_Chi_Minh"):
    """
    Trả về chuỗi thông tin về ngữ cảnh thời gian hiện tại.
    Hàm này tạo ra một chuỗi chứa thông tin về các ngày liên quan đến thời điểm hiện tại,
    bao gồm:
    - Ngày hôm kia, hôm qua, hôm nay, ngày mai, ngày kia
    - Ngày trong tuần hiện tại (ví dụ: "Thứ 2")
    - Ngày bắt đầu của tuần này và tuần sau
    - Danh sách các ngày trong tuần này và tuần sau với tên tiếng Việt
    Thông tin này được thiết kế để sử dụng trong việc trích xuất thời gian từ văn bản
    tiếng Việt khi cần ngữ cảnh về thời điểm hiện tại.
    Parameters
    ----------
    timezone : str, optional
        Múi giờ được sử dụng để tính toán thời gian, mặc định là 'Asia/Ho_Chi_Minh'
    Returns
    -------
    str
        Chuỗi chứa thông tin ngữ cảnh thời gian được định dạng dưới dạng văn bản
    """

    now = datetime.now(pytz.timezone(timezone))

    # Calculate relevant dates
    yesterday = now - timedelta(days=1)
    day_before_yesterday = now - timedelta(days=2)
    tomorrow = now + timedelta(days=1)
    day_after_tomorrow = now + timedelta(days=2)
    this_week = now - timedelta(days=now.weekday())
    next_week = this_week + timedelta(days=7)

    # Dictionary for Vietnamese weekday names
    vn_weekdays = {
        0: "Thứ 2",
        1: "Thứ 3",
        2: "Thứ 4",
        3: "Thứ 5",
        4: "Thứ 6",
        5: "Thứ 7",
        6: "Chủ nhật",
    }

    # Get weekdays for current and next week using the utility function
    weekdays_list = get_weekdays_context(timezone)

    # Format weekday strings
    weekday_str = "\n    ".join(
        [
            f"- {vn_weekdays[day.weekday()]} của tuần {'này' if day < next_week else 'sau'}: {day.strftime('%Y-%m-%d')}"
            for day in weekdays_list[7:]
        ]
    )

    # Get past days of current week
    past_days_str = "\n    ".join(
        [
            f"- {vn_weekdays[day.weekday()]}: {day.strftime('%Y-%m-%d')}"
            for day in weekdays_list[:7]
            if day.date() < now.date()
        ]
    )

    return f"""
    Áp dụng thông tin thời gian thực dưới đây để trích xuất thời gian chính xác:
    - Hôm kia: {day_before_yesterday.strftime('%Y-%m-%d')}
    - Hôm qua: {yesterday.strftime('%Y-%m-%d')}
    - Hôm nay: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}
    - Ngày mai: {tomorrow.strftime('%Y-%m-%d')}
    - Ngày kia: {day_after_tomorrow.strftime('%Y-%m-%d')}
    - Ngày trong tuần hiện tại: {vn_weekdays[now.weekday()]}
    - Tuần này bắt đầu từ: {this_week.strftime('%Y-%m-%d')}
    - Tuần sau bắt đầu từ: {next_week.strftime('%Y-%m-%d')}
    - Các ngày trong tuần này đã qua(không sử dụng chúng): 
    {past_days_str}
    Tham chiếu các ngày trong tuần sau:
    {weekday_str}"""


def get_today_tomorrow(timezone: str = "Asia/Ho_Chi_Minh"):
    """
    Hàm get_today_tomorrow lấy ngày hôm nay và ngày mai theo múi giờ đã cho.
    Tham số:
        timezone (str): Múi giờ để xác định thời gian hiện tại. Mặc định là 'Asia/Ho_Chi_Minh'.
    Trả về:
        Tuple[str, str]: Một tuple chứa hai chuỗi đại diện cho ngày hôm nay và ngày mai
        với định dạng "YYYY-MM-DD".
    """
    now = datetime.now(pytz.timezone(timezone))
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    return today, tomorrow


def get_valid_weekday(target_date, timezone: str = "Asia/Ho_Chi_Minh"):
    """
    Kiểm tra và điều chỉnh ngày được chỉ định để đảm bảo nó là một ngày trong tương lai.
    Nếu ngày đã qua (nhỏ hơn hoặc bằng thời gian hiện tại), hàm sẽ thêm 7 ngày vào
    ngày đó để đặt nó vào tuần sau.
    Parameters
    ----------
    target_date : datetime
        Ngày cần kiểm tra
    timezone : str, optional
        Múi giờ để so sánh với thời gian hiện tại, mặc định là 'Asia/Ho_Chi_Minh'
    Returns
    -------
    datetime
        Ngày hợp lệ (đảm bảo là trong tương lai)
    """

    now = datetime.now(pytz.timezone(timezone))
    if target_date <= now:  # Nếu ngày đã qua
        return target_date + timedelta(days=7)
    return target_date


import ast
import json
def parse_to_dict(s):
    """
    Chuyển chuỗi s (có thể là JSON-string hoặc Python‐dict‐like string) thành dict.
    Nếu s đã là dict thì trả về nguyên bản.
    """
    if isinstance(s, dict):
        return s
    if not isinstance(s, str):
        raise ValueError(f"Unsupported type: {type(s)}")
    # Thử JSON trước
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # Nếu không phải JSON, dùng ast.literal_eval để parse Python literal
        try:
            return ast.literal_eval(s)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Cannot parse string to dict: {e}")
        
# from langchain_core.chat_history import InMemoryChatMessageHistory
# def create_history_from_list(message_list):
#     'Chuyển đổi danh sách tin nhắn thành lịch sử hội thoại'
#     history = InMemoryChatMessageHistory()
#     for msg in message_list:
#         if msg["type"] == "user":
#             history.add_user_message(msg["content"])
#         elif msg["type"] == "assistant":
#             history.add_ai_message(msg["content"])
#     return history

from langchain.schema import HumanMessage, AIMessage, BaseMessage
def convert_list_to_messages(chat_history_raw) -> list[BaseMessage]:
    messages = []
    for item in chat_history_raw:
        role = item.get("type")
        content = item.get("content")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
    return messages

# ============ Fucntions helper for web ============
def convert_chat_history_to_html(chat_history):
    """Convert chat history messages to HTML using markdown2"""
    import markdown2
    chat_history_html = []
    for message in chat_history:
        if isinstance(message, dict) and "content" in message:
            content_html = markdown2.markdown(message["content"].replace("\n", "<br>"), extras=["autolink"])
            chat_history_html.append({
                "type": message.get("type", ""),
                "content": content_html
            })
        else:
            chat_history_html.append(message)
    return chat_history_html

def format_timezone(conversations,router=None):
    """Convert datetime to Vietnam timezone for frontend"""
    for conv in conversations:
        if "updated_at" in conv and isinstance(conv["updated_at"], datetime):
            vietnam_time = conv["updated_at"] + timedelta(hours=7)
            if router == "index":
                conv["updated_at"] = vietnam_time
            else:
                conv["updated_at"] = vietnam_time.strftime("%Y-%m-%dT%H:%M:%S+07:00")
    return conversations