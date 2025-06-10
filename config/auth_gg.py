# from google.oauth2 import service_account
# from googleapiclient.discovery import build
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# from .environment import CALENDAR_ID, CLIENT_SECRET_FILE, SCOPES
from dotenv import load_dotenv
load_dotenv()
# Lấy các biến ra từ file .env
CALENDAR_ID = os.getenv("CALENDAR_ID")
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
# Scope cho quyền truy cập vào Google Calendar và Gmail API
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://mail.google.com/"
]

# def xac_thuc_calendar():
#     """
#     Hàm xác thực và kết nối với Google Calendar API.
#     Trả về đối tượng dịch vụ để tương tác với Google Calendar.
#     """
#     # Tạo đối tượng credentials từ tệp JSON của Service Account
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES)

#     # Kết nối với Google Calendar API
#     service = build('calendar', 'v3', credentials=credentials)

#     return service,CALENDAR_ID


TOKEN_FILE = "token.json"
def xac_thuc_google():
    creds = None
    # Load token đã lưu nếu có
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # Nếu không có token hoặc token hết hạn thì đăng nhập lại
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Lưu token mới vào file
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def xac_thuc_calendar():
    creds = xac_thuc_google()
    service = build("calendar", "v3", credentials=creds)
    return service, CALENDAR_ID


def xac_thuc_gmail():
    creds = xac_thuc_google()
    service = build("gmail", "v1", credentials=creds)
    return service