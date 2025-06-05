from config.calendar import xac_thuc_gmail
import base64
from email import message_from_bytes
from utils import to_utc_timestamp

service = xac_thuc_gmail()
def get_mail_in_range(query):
    """Lấy danh sách mail (không chứa 'Re:') trong khoảng thời gian (chỉ ở mục Primary)."""
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
        content = get_email_content(msg['id'])
        from datetime import datetime
        sent_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        mail_list.append({
            'id': msg['id'],
            'subject': subject,
            'from': sender,
            'content': content,
            'time': sent_time
        })
    return mail_list


def get_email_content(message_id):
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

from concurrent.futures import ThreadPoolExecutor
from services.llm.llm_config import llm_summarize

def summarize_mails(mails):
    chain_summarize_1 = llm_summarize(option_api=2)
    chain_summarize_2 = llm_summarize(option_api=3)
    chain_summarize_3 = llm_summarize(option_api=4)

    n = len(mails)
    part1 = mails[:n // 3]
    part2 = mails[n // 3: 2 * n // 3]
    part3 = mails[2 * n // 3:]
    print(f"[*] Số lượng mail: {n}, Chia thành 3 phần: {len(part1)}, {len(part2)}, {len(part3)}")

    def invoke_chain(chain, emails):
        print('Đang tóm tắt emails...')
        return chain.invoke({"mails": emails}).content

    summaries = []
    with ThreadPoolExecutor() as executor:
        futures = []

        if part1:
            futures.append(executor.submit(invoke_chain, chain_summarize_1, part1))
        else:
            summaries.append("--- Bản tóm tắt 1 ---\n(Không có email)\n\n")

        if part2:
            futures.append(executor.submit(invoke_chain, chain_summarize_2, part2))
        else:
            summaries.append("--- Bản tóm tắt 2 ---\n(Không có email)\n\n")

        if part3:
            futures.append(executor.submit(invoke_chain, chain_summarize_3, part3))
        else:
            summaries.append("--- Bản tóm tắt 3 ---\n(Không có email)\n\n")

        # Lấy kết quả từ futures theo thứ tự ban đầu
        for idx, future in enumerate(futures):
            summaries.append(f"--- Bản tóm tắt {idx+1} ---\n{future.result()}\n\n")

    summaries.append("Hãy gộp 3 bản tóm tắt này lại với nhau để tạo thành một bản tóm tắt hoàn chỉnh cho người dùng.")
    return "\n".join(summaries)

from utils import parse_to_dict
def summarize_emails_api(args, limit=8):
    """Tổng hợp context mail trong khoảng thời gian đã cho."""
    args = parse_to_dict(args)
    #Chuyển thời gian sang timezone UTC
    query = []
    query.append("-subject:Re")  # Loại bỏ các email đã trả lời
    query.append("category:primary")  # Chỉ lấy email trong mục Primary
    if args['sender']:
        query.append(f"from:{args['sender']}")
    if args['subject']:
        query.append(f"subject:{args['subject']}")
    if args['keyword']:
        query.append(f"{args['keyword']}")
    if args['start_date']:
        query.append(f"after:{to_utc_timestamp(args['start_date'])}")
    if args['end_date']:
        query.append(f"before:{to_utc_timestamp(args['end_date'])}")
    #Tạo bộ lọc query
    query = " ".join(query)
    print(f"[*] Truy vấn tìm kiếm: {query}")
    mails = get_mail_in_range(query)
    if limit:
        mails = mails[:limit]
    # return len(mails)
    return summarize_mails(mails)

