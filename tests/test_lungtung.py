import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

# from bot.agent_calendar import *
# from features import *
# data = '{"title_old": "đi chơi", "title_new": "học nhóm", "location_old": "trường", "location_new": "trường", "datetime_ranges": [{"start_datetime": "2025-05-27 08:00:00", "end_datetime": "2025-05-27 08:00:01", "start_new": "2025-05-27 08:00:00", "end_new": "2025-05-27 08:00:00"}], "incorrect_datetime": False}'
# print(update_event_api(data))
from config.calendar import xac_thuc_gmail
service = xac_thuc_gmail()
import base64
import re
from email import message_from_bytes


def get_mail_in_range(service, start_date, end_date):
    """Lấy danh sách mail (không chứa 'Re:') trong khoảng thời gian (chỉ ở mục Primary)."""
    query = f"after:{start_date} before:{end_date} -subject:Re category:primary from:'Bảo ngọc' subject:'phỏng vấn'"
    response = service.users().messages().list(userId='me', q=query).execute()
    messages = response.get('messages', [])

    mail_list = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        # Trích xuất subject và sender từ headers
        headers = msg_detail.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "")
        timestamp = int(msg_detail.get("internalDate", 0))  # milliseconds
        # content = get_email_content(service, msg['id'])
        from datetime import datetime
        sent_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        mail_list.append({
            'id': msg['id'],
            'subject': subject,
            'from': sender,
            # 'content': content,
            'time': sent_time
        })
    return mail_list


def get_email_content(service, message_id):
    """Trích xuất nội dung text từ mail (ưu tiên plain text, fallback html)."""
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
        raw_data = base64.urlsafe_b64decode(message['raw'])
        email_msg = message_from_bytes(raw_data)

        content = ""
        if email_msg.is_multipart():
            for part in email_msg.walk():
                ctype = part.get_content_type()
                if ctype in ["text/plain", "text/html"] and "attachment" not in str(part.get("Content-Disposition")):
                    charset = part.get_content_charset() or "utf-8"
                    content = part.get_payload(decode=True).decode(charset, errors="replace")
                    if ctype == "text/plain":
                        break  # Ưu tiên plain text
        else:
            charset = email_msg.get_content_charset() or "utf-8"
            content = email_msg.get_payload(decode=True).decode(charset, errors="replace")

        return content
    except Exception as e:
        print(f"[!] Lỗi khi lấy nội dung mail: {e}")
        return ""

# from bs4 import BeautifulSoup
# def clean_email_content(content):
#     soup = BeautifulSoup(content, 'html.parser')
#     text = soup.get_text(separator=' ')
#     return ' '.join(text.split())

from services.llm.llm_config import llm_gen
llm = llm_gen(temperature=0.0)
from langchain.prompts import PromptTemplate
prompt_template = """Bạn là một trợ lý ảo thông minh có khả năng tóm tắt nội dung email. Bạn sẽ nhận vào một danh sách các email và trả về nội dung tóm tắt của chúng kèm các thông tin về subject.
Nếu chúng có các thông tin ngày tháng, địa điểm(các nội dung có thể tạo lịch) thì đưa ra các thông tin đó cho người dùng biết
Dưới đây là danh sách các email:
{mails}
Bạn cần tóm tắt nội dung của các email này và trả về một danh sách các câu tóm tắt để người dùng có thể hiểu nhanh nội dung của chúng. Mỗi câu tóm tắt nên ngắn gọn và súc tích, chỉ bao gồm các thông tin quan trọng nhất.
Nếu có các thông tin về ngày tháng, địa điểm trong nội dung email thì hãy đưa ra các thông tin đó cho người dùng biết."""
prompt = PromptTemplate(
    input_variables=["mails"],
    template=prompt_template
)
chain_summarize = prompt | llm

def get_context_mail_api(service,args, limit=10):
    """Tổng hợp context mail trong khoảng thời gian đã cho."""
    mails = get_mail_in_range(service, args["start_date"], args["end_date"])
    if limit:
        mails = mails[:limit]
    return mails
    # return chain_summarize.invoke({"mails": mails}).content

args = {
    "start_date": "2025-05-08",
    "end_date": "2025-05-11",
    "from": "Bảo Ngọc",
}
print(get_context_mail_api(service,args))