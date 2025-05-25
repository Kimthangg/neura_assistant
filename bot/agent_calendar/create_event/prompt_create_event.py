from utils.helpers import (
    get_next_valid_date,
    get_today_tomorrow,
    get_valid_weekday,
    get_weekdays_context,
)


def create_event_normal():
    today, tomorrow = get_today_tomorrow()
    weekdays = get_weekdays_context()
    return f"""
Hãy tuân theo các hướng dẫn sau để trích xuất thông tin sự kiện thông thường:
1. Xác thực câu truy vấn của người dùng:
Kiểm tra xem thời gian có thỏa mãn điều kiện(incorrect_datetime):
    - Kiểm tra ngày không hợp lệ: ví dụ 30/2, 31/4, 31/6, 31/9, 31/11,..., Lưu ý rằng tháng 2 có thể có 28 hoặc 29 ngày tùy thuộc vào năm nhuận.
    - Kiểm tra thời gian không hợp lệ: ví dụ 24:00:00, 25:00:00,..
    - Kiểm tra tháng không hợp lệ: ví dụ Tháng 13, tháng 0,...
    - Kiểm tra năm không hợp lệ: < năm hiện tại
    - Mặc định là False chỉ trả về True nếu tìm thấy bất kỳ mẫu không hợp lệ nào
2. Trích xuất tiêu đề sự kiện từ yêu cầu
 - Trích xuất thông tin về sự kiện từ câu lệnh của người dùng.
 - Example: 
    * "Họp nhóm" từ "Tạo sự kiện họp nhóm vào ngày mai lúc 15h"
    * "Đi chơi" từ "Tạo sự kiện đi chơi vào cuối tuần"
    * "Học Toeic" từ "Tạo sự kiện học Toeic vào tối thứ 7"
3. Trích xuất thời gian được đề cập:
  - Trích xuất tất cả các khoảng ngày giờ được đề cập trong văn bản một cách chính xác.
  - Chuyển đổi sang định dạng ISO chuẩn (YYYY-MM-DD HH:mm:ss).
  - Xử lý các mốc thời gian tương đối (hôm nay, ngày mai, tuần sau, v.v.) dựa vào các mốc thời gian đã đề cập, nếu thời gian đã qua thì lấy tuần sau.
  - Chú ý xử lý thời gian các ngày trong tuần(thứ ba tuần này, thứ 5 tuần sau, v.v.):
    + Nếu ngày đó là ngày hôm nay thì sử dụng tuần sau
    + Nếu ngày đó là ngày đã qua thì sử dụng tuần sau
    + Nếu ngày đó chưa đến thì sử dụng tuần này
    ==> Sử dụng thời gian hiện tại đã đề cập để tùy chỉnh cho chính xác
  - Nếu chỉ có ngày mà không có giờ, sử dụng 00:00:00 cho thời điểm bắt đầu và 23:59:59 cho thời điểm kết thúc.
  - Nếu chỉ có một mốc thời gian duy nhất, đặt nó làm cả thời điểm bắt đầu và kết thúc (thời gian bắt đầu bằng thời gian kết thúc).
  - Trích xuất địa điểm sự kiện nếu được đề cập, nếu không có thì để trống ('').
  - Trích xuất quy tắc lặp lại (RRULE) từ yêu cầu của người dùng, đảm bảo tuân theo định dạng iCalendar:
    + FREQ: tần suất (DAILY, WEEKLY, MONTHLY, YEARLY)
    + INTERVAL: khoảng cách (mặc định là 1)
    + BYMONTHDAY: ngày trong tháng (1-31)
    + BYMONTH: tháng trong năm (1-12)
    + BYDAY: ngày trong tuần (MO, TU, WE, TH, FR, SA, SU)
    + COUNT: số lần lặp lại
    + UNTIL: ngày kết thúc lặp lại (YYYYMMDD)
  - Chỉ lấy thời gian của ngày đầu tiên trong khoảng thời gian được đề cập.
  ("Tôi vừa đăng kí học Toeic ở Toeic Thầy Long vào 7h tối vào thứ 2, thứ 4, thứ 6 hàng tuần cho đến ngày 25 tháng 6" sẽ đưa ra datetime_ranges là thứ 2 từ 19:00:00 đến 19:00:00 và rrule là RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20250625")
  - Trong các trường hợp không rõ ràng, đưa ra giả định hợp lý dựa trên ngữ cảnh.
  - Trả về một mảng rỗng nếu không tìm thấy thông tin ngày giờ nào.
4. Trích xuất cài đặt nhắc nhở (reminders) từ yêu cầu của người dùng:
  - Xác định xem có sử dụng cài đặt mặc định của lịch không (usedefault = true/false).
  - Nếu người dùng không đề cập gì về nhắc nhở, mặc định sẽ sử dụng cài đặt mặc định (usedefault = true).
  - Nếu người dùng muốn tùy chỉnh nhắc nhở:
    + Trích xuất số phút trước khi sự kiện diễn ra (minutes).
    + Phương thức nhắc nhở (method) chỉ hỗ trợ "popup".
    + Ví dụ: "nhắc trước 30 phút", "gửi thông báo trước 1 tiếng", "báo trước 15 phút"...
  - Trả về một đối tượng reminders với cấu trúc:
    + usedefault: boolean (true/false)
    + overrides: mảng các nhắc nhở tùy chỉnh (rỗng nếu usedefault = true)
      * method: "popup"
      * minutes: số phút trước sự kiện (5, 10, 15, 30, 60, ...)
  - Nếu người dùng chỉ định nhiều nhắc nhở khác nhau, thêm tất cả vào mảng overrides.
IMPORTANT: KHÔNG SỬ DỤNG THỜI GIAN TRONG QUÁ KHỨ
Ví dụ 1: 
Input: "Ngày 15/05 tôi có buổi thi trên trường vào lúc 10 giờ sáng hãy tạo lịch."
Output:
{{
  'title': 'Buổi thi',
  'incorrect_datetime': False,
  'datetime_ranges': [
    {{
      'start_datetime': '{today.replace(day=15, month=5).strftime("%Y-%m-%d")} 10:00:00', 
      'end_datetime': '{today.replace(day=15, month=5).strftime("%Y-%m-%d")} 10:00:00',
      'rrule': ''
    }}
  ], 
  'location': 'trường',
  'reminders': {{
    'usedefault': True,
    'overrides': []
  }}
}}

Ví dụ 2:
Input: "Tạo lịch họp ngày mai từ 14h đến 16h tại phòng A1-501"
Output:
{{
  'title': 'Họp',
  'incorrect_datetime': False,
  'datetime_ranges': [
    {{
      'start_datetime': '{tomorrow.strftime("%Y-%m-%d")} 14:00:00',
      'end_datetime': '{tomorrow.strftime("%Y-%m-%d")} 16:00:00',
      'rrule': ''
    }}
  ],
  'location': 'phòng A1-501',
  'reminders': {{
    'usedefault': True,
    'overrides': []
  }}
}}

Ví dụ 3:
Input: "Đặt lịch hẹn với bác sĩ vào 9h sáng thứ Sáu tuần này và nhắc tôi trước 30 phút"
Output:
{{
  'title': 'Lịch hẹn với bác sĩ',
  'incorrect_datetime': False,
  'datetime_ranges': [
    {{
      'start_datetime': '{weekdays[4].strftime("%Y-%m-%d")} 09:00:00',
      'end_datetime': '{weekdays[4].strftime("%Y-%m-%d")} 09:00:00',
      'rrule': ''
    }}
  ],
  'location': '',
  'reminders': {{
    'usedefault': False,
    'overrides': [
      {{
        'method': 'popup',
        'minutes': 30
      }}
    ]
  }}
}}

Ví dụ 4: 
Input: "Tôi có một cuộc họp vào mỗi thứ Hai từ 10 giờ sáng đến 11 giờ sáng, nhắc trước 15 phút và 1 giờ"
Output:
{{
  'title': 'Cuộc họp',
  'incorrect_datetime': False,
  'datetime_ranges': [
    {{
      'start_datetime': '{get_valid_weekday(weekdays[0]).strftime("%Y-%m-%d")} 10:00:00', 
      'end_datetime': '{get_valid_weekday(weekdays[0]).strftime("%Y-%m-%d")} 11:00:00',
      'rrule': 'RRULE:FREQ=WEEKLY;BYDAY=MO'
    }}
  ], 
  'location': '',
  'reminders': {{
    'usedefault': False,
    'overrides': [
      {{
        'method': 'popup',
        'minutes': 15
      }},
      {{
        'method': 'popup',
        'minutes': 60
      }}
    ]
  }}
}}

Ví dụ 5:
Input: "Tạo sự kiện hàng tháng vào ngày 15 từ 2 giờ đến 3 giờ chiều tại Văn phòng công ty"
Output:
{{
  'title': 'Sự kiện hàng tháng',
  'incorrect_datetime': False,
  'datetime_ranges': [
    {{
      'start_datetime': '{get_next_valid_date(15).strftime("%Y-%m-%d")} 14:00:00',
      'end_datetime': '{get_next_valid_date(15).strftime("%Y-%m-%d")} 15:00:00',
      'rrule': 'RRULE:FREQ=MONTHLY;BYMONTHDAY=15'
    }}
  ],
  'location': 'Văn phòng công ty',
  'reminders': {{
    'usedefault': True,
    'overrides': []
  }}
}}

Ví dụ 6:
Input: "Tạo lịch họp hằng năm vào ngày 30/04 lúc 8 giờ sáng và báo trước 1 ngày"
Output:
{{
  'title': 'Lịch họp hằng năm',
  'incorrect_datetime': False,
  'datetime_ranges': [
    {{
      'start_datetime': '{today.replace(day=30, month=4).strftime("%Y-%m-%d")} 08:00:00',
      'end_datetime': '{today.replace(day=30, month=4).strftime("%Y-%m-%d")} 08:00:00',
      'rrule': 'RRULE:FREQ=YEARLY;BYMONTHDAY=30;BYMONTH=4'
    }}
  ],
  'location': '',
  'reminders': {{
    'usedefault': False,
    'overrides': [
      {{
        'method': 'popup',
        'minutes': 1440
      }}
    ]
  }}
}}
"""
