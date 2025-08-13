# Neura - Trợ lý cá nhân AI

Neura là một trợ lý cá nhân AI đa năng giúp người dùng quản lý lịch, sự kiện, email và lên lịch cho các tác vụ tự động thông qua giao diện chat trực quan. Ứng dụng sử dụng kỹ thuật xử lý ngôn ngữ tự nhiên (NLP) và Mô hình ngôn ngữ lớn (LLM) để hiểu yêu cầu của người dùng và thực hiện các thao tác với Google Calendar và Gmail.

## Tổng quan hệ thống

![Neura System Diagram](neura_diagram.png)

Hệ thống Neura được chia thành các phần chính sau:

1. **Frontend**: Giao diện người dùng dạng chat trực quan (Web + Telegram)
2. **Backend**: Xử lý logic nghiệp vụ, tương tác với API bên ngoài và xử lý ngôn ngữ tự nhiên
3. **LLM Service**: Dịch vụ mô hình ngôn ngữ lớn (Gemini Pro)
4. **External APIs**: Tích hợp với Google Calendar và Gmail
5. **Database**: MongoDB để lưu trữ lịch sử chat, thông tin tác vụ

## Tính năng chính

### 1. Quản lý Lịch (Calendar)

- Tạo sự kiện mới
- Xem lịch trong khoảng thời gian cụ thể
- Cập nhật thông tin sự kiện
- Xóa sự kiện
- Tìm thời gian rảnh
- Lấy thông tin nhiều lịch trong một khoảng thời gian

### 2. Quản lý Email (Gmail)

- Tóm tắt email trong khoảng thời gian cụ thể
- Trích xuất thông tin từ email để tạo sự kiện lịch
- Cảnh báo email có deadline gần đến hạn
- Tìm kiếm email thông minh với nội dung cụ thể

### 3. Lập lịch tự động

- Lên lịch cho các tác vụ tự động
- Quản lý và hủy các tác vụ đã lên lịch
- Liệt kê các tác vụ đã lên lịch

### 4. Hỗ trợ đa nền tảng

- Giao diện web
- Bot Telegram

## Cấu trúc dự án

```
├── app/                       # Ứng dụng Flask web
│   ├── app.py                 # Điểm khởi đầu ứng dụng web
│   ├── static/                # Tài nguyên tĩnh (CSS, JS, Images)
│   └── templates/             # Templates HTML
├── bot/                       # Module xử lý chatbot
│   ├── agent/                 # Quản lý các agent
│   │   ├── agent_calendar.py  # Xử lý tác vụ calendar
│   │   ├── agent_gmail.py     # Xử lý tác vụ email
│   │   ├── agent_manager.py   # Quản lý, phân loại ý định
│   │   ├── bot_telegram.py    # Bot Telegram
│   │   └── schedule_task.py   # Quản lý tác vụ lịch trình
│   ├── agent_intent/          # Xử lý ý định người dùng
│   │   ├── prompt.py          # Mẫu nhắc cho LLM
│   │   └── tools.py           # Công cụ xử lý ý định
│   └── handler/               # Xử lý luồng tin nhắn
│       ├── message.py         # Xử lý tin nhắn
│       └── retrieval_infomation.py # Truy xuất thông tin
├── config/                    # Cấu hình hệ thống
│   ├── auth_gg.py             # Xác thực Google API
│   ├── environment.py         # Biến môi trường
│   └── mongodb.py             # Cấu hình MongoDB
├── db/                        # Quản lý cơ sở dữ liệu
│   ├── base_manager.py        # Lớp quản lý cơ bản
│   ├── chat_manager.py        # Quản lý lịch sử chat
│   ├── db_manager.py          # Tương tác với MongoDB
│   ├── email_manager.py       # Quản lý dữ liệu email
│   └── schedule_manager.py    # Quản lý lịch trình
├── features/                  # Các tính năng chính của ứng dụng
│   ├── calendar_features/     # Tính năng quản lý lịch
│   │   ├── create_calendar/   # Tạo sự kiện
│   │   ├── delete_calendar/   # Xóa sự kiện
│   │   ├── get_calendar/      # Xem lịch
│   │   └── update_calendar/   # Cập nhật sự kiện
│   ├── gmail_features/        # Tính năng quản lý email
│   │   └── summarize_emails/  # Tóm tắt email
│   └── schedule_features/     # Tính năng lập lịch tự động
│       ├── handler.py         # Xử lý tác vụ lịch trình
│       ├── prompt.py          # Mẫu nhắc cho lịch trình
│       └── tools.py           # Công cụ lập lịch
├── services/                  # Các dịch vụ bên ngoài
│   ├── embedding_model/       # Mô hình embedding
│   │   └── embedding.py       # Dịch văn bản thành vector
│   └── llm/                   # Dịch vụ mô hình ngôn ngữ lớn
│       └── llm_config.py      # Cấu hình LLM
├── utils/                     # Tiện ích và công cụ chung
│   ├── default_text.py        # Văn bản mặc định cho chatbot
│   └── helpers.py             # Hàm trợ giúp
└── main.py                    # Điểm khởi đầu ứng dụng
```

## Các thành phần chính

1. **Agent Management**: Hệ thống quản lý các agent chuyên biệt
   - Agent Manager: Phân tích ý định người dùng, điều phối và chọn agent phù hợp với yêu cầu
   - Agent Calendar: Xử lý các tác vụ liên quan đến lịch
   - Agent Gmail: Xử lý các tác vụ liên quan đến email

2. **Handler**: Quản lý luồng tin nhắn và tương tác
   - Xử lý tin nhắn đầu vào
   - Tạo phản hồi phù hợp

3. **Services**: Kết nối với các dịch vụ bên ngoài
   - Tương tác với Google Calendar API
   - Tương tác với Gmail API
   - Tích hợp mô hình ngôn ngữ lớn (LLM) - Gemini Pro
   - Embedding Model - Halong Embedding

4. **Database**: Lưu trữ lịch sử hội thoại và thông tin người dùng
   - Sử dụng MongoDB để lưu trữ dữ liệu

## Công nghệ sử dụng

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB
- **LLM**: Gemini Pro
- **Embedding Model**: Halong Embedding
- **APIs**: Google Calendar API, Gmail API
- **Bot Platform**: Telegram Bot API
- **Task Scheduling**: APScheduler
- **Dependency Management**: pip, requirements.txt

## Yêu cầu hệ thống

- Python 3.10+
- MongoDB

## Cài đặt

1. Clone repository:

```bash
git clone https://github.com/Kimthangg/neura_assistant.git
cd neura_assistant
```

2. Cài đặt các gói phụ thuộc:

```bash
pip install -r requirements.txt
```

3. Thiết lập các biến môi trường (tạo file `.env`):

```
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
DB_NAME=neura
COLLECTION_NAME=chat_history

# Google API Credentials
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# LLM Configuration
API_KEY=your_api_key
API_BASE=your_api_base
MODEL_NAME=your_model_name

# Telegram Bot
BOT_TOKEN=your_bot_token
```

4. Xác thực với Google API:
   - Đặt file `credentials.json` vào thư mục gốc
   - Chạy script xác thực để tạo `token.json`

## Chạy ứng dụng

Chạy cả hai ứng dụng (Web và Telegram Bot):

```bash
python main.py
```

Hoặc chạy riêng ứng dụng web:

```bash
python -m app.app
```

Hoặc chạy riêng bot Telegram:

```bash
python -m bot.agent.bot_telegram
```

## Cách sử dụng

### Web Interface
1. Truy cập `http://localhost:5000` trong trình duyệt
2. Bắt đầu chat với trợ lý Neura
3. Gõ các câu lệnh tự nhiên như:
   - "Tạo lịch họp với team vào ngày mai lúc 10h sáng"
   - "Tóm tắt email trong 3 ngày qua"
   - "Lên lịch nhắc nhở tôi họp hằng tuần vào thứ 2 lúc 9h"

### Telegram Bot
1. Tìm bot của bạn trên Telegram theo username đã đăng ký
2. Bắt đầu chat với bot bằng cách gõ `/start`
3. Gõ các câu lệnh tự nhiên tương tự như trên web interface

## Luồng hoạt động của hệ thống

1. **Người dùng nhập yêu cầu**:
   - Ví dụ Calendar: "Tạo lịch họp với team vào 2h chiều mai tại phòng 301"
   - Ví dụ Gmail: "Tìm và tóm tắt các email từ trưởng phòng trong tuần này"

2. **Frontend gửi yêu cầu tới Backend**:
   - Gửi POST request đến endpoint `/chat`
   - Hiển thị hiệu ứng "đang nhập" cho người dùng

3. **Backend xử lý yêu cầu**:
   - Gửi yêu cầu trực tiếp đến agent_manager
   - Agent Manager phân tích ý định và chọn agent phù hợp (agent_calendar hoặc agent_gmail)
   - Trích xuất thông tin (ngày, giờ, người tham gia, từ khóa tìm kiếm...)
   - Tạo phản hồi dựa trên kết quả xử lý

4. **Phản hồi đến người dùng**:
   - Backend trả về JSON chứa phản hồi và trạng thái
   - Frontend hiển thị phản hồi với hiệu ứng gõ văn bản
   - Nếu cần xác nhận hành động, hiển thị nút "Thực hiện"

5. **Thực hiện hành động (nếu có)**:
   - Khi người dùng nhấn "Thực hiện", gửi request đến `/execute`
   - Backend thực hiện hành động với API tương ứng (Google Calendar hoặc Gmail)
   - Trả về kết quả thành công hoặc thất bại

6. **Lưu hội thoại**:
   - Lưu lịch sử hội thoại vào MongoDB
   - Cập nhật danh sách hội thoại trong giao diện

## Đóng góp

Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) để biết chi tiết về quy trình đóng góp code.

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## Tác giả

- Kimthangg
