# Neura - Trợ lý cá nhân AI

Neura là một trợ lý cá nhân AI đa năng giúp người dùng quản lý lịch, sự kiện và email thông qua giao diện chat trực quan. Ứng dụng sử dụng kỹ thuật xử lý ngôn ngữ tự nhiên (NLP) để hiểu yêu cầu của người dùng và thực hiện các thao tác với Google Calendar và Gmail.

## Tổng quan hệ thống

Hệ thống Neura được chia thành hai phần chính:

1. **Backend**: Xử lý logic nghiệp vụ, tương tác với API bên ngoài và xử lý ngôn ngữ tự nhiên
2. **Frontend**: Giao diện người dùng dạng chat trực quan

```ascii
┌─────────────────────────────────────────────────────────────────────────┐
│                            NEURA SYSTEM                                  │
├───────────────┐                                 ┌─────────────────────┐  │
│               │                                 │                     │  │
│   Frontend    │                                 │    External APIs    │  │
│   (Browser)   │                                 │                     │  │
│     ┌─────────┴─────────┐                       │   ┌─────────────┐   │  │
│     │                   │                       │   │   Google    │   │  │
│     │  Web Interface    │                       │   │  Calendar   │   │  │
│     │    (HTML/CSS/JS)  │                       │   │     API     │   │  │
│     └─────────┬─────────┘                       │   └──────┬──────┘   │  │
│               │                                 │          │          │  │
│               │  HTTP Requests                  │   ┌─────────────┐   │  │
│               │                                 │   │   Google    │   │  │
├───────────────┼─────────────────────────────────┤   │   Gmail     │   │  │
│               │                                 │   │     API     │   │  │
│               ▼                                 │   └──────┬──────┘   │  │
│     ┌───────────────────┐                       │          │          │  │
│     │                   │                       │          │          │  │
│     │   Flask Server    │◄──────────────────────┼──────────┘          │  │
│     │   (app/app.py)    │                       │                     │  │
│     │                   │                       │                     │  │
│     └────────┬──────────┘                       │                     │  │
│              │                                  │                     │  │
│              │                                  │                     │  │
│              ▼                                  │                     │  │
│    ┌────────────────────┐                       │                     │  │
│    │                    │                       │                     │  │
│    │ Bot Module         │                       │                     │  │
│    │ ┌────────────────┐ │         ┌─────────────────┐                │  │
│    │ │ Agent Manager  │ │         │                 │                │  │
│    │ │(Intent & Route)│ │         │  LLM Service   │                │  │
│    │ └────────────────┘ │◄────────┤  (Gemini 2.0)  │                │  │
│    │ ┌────────────────┐ │         │                 │                │  │
│    │ │Agent Extraction│ │         └─────────────────┘                │  │
│    │ │(Data Extraction)│ │                                           │  │
│    │ └────────────────┘ │                                            │  │
│    │ ┌────────────────┐ │                                            │  │
│    │ │    Handler     │ │                                            │  │
│    │ │(Message Flow)  │◄├────────────────────────────────────────────┘  │
│    │ └────────────────┘ │                                               │
│    └──────────┬─────────┘                                               │
│               │                                                         │
│               │                                                         │
│               ▼                                                         │
│     ┌───────────────────┐                                               │
│     │                   │                                               │
│     │     MongoDB       │                                               │
│     │    Database       │                                               │
│     │                   │                                               │
│     └───────────────────┘                                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Backend

Backend của Neura được xây dựng bằng Python với Flask framework và tích hợp các công nghệ sau:

### Cấu trúc Backend

```plaintext
├── app.py                     # Điểm khởi đầu ứng dụng Flask 
├── bot/                       # Các module xử lý logic chatbot
│   ├── agent/                 # Quản lý các agent
│   │   ├── agent_calendar.py  # Xử lý các tác vụ calendar
│   │   ├── agent_gmail.py     # Xử lý các tác vụ email
│   │   └── agent_manager.py   # Quản lý, phân loại ý định và điều phối các agent
│   └── handler/               # Xử lý luồng tin nhắn
├── config/                    # Cấu hình hệ thống
│   ├── calendar.py            # Cấu hình Google Calendar API
│   ├── environment.py         # Biến môi trường
│   └── mongodb.py             # Cấu hình MongoDB
├── db/                        # Quản lý cơ sở dữ liệu
│   └── db_manager.py          # Tương tác với MongoDB
├── features/                  # Các tính năng chính của ứng dụng
│   ├── calendar_features/     # Tính năng quản lý lịch
│   │   ├── create_calendar/   # Tạo sự kiện
│   │   ├── delete_calendar/   # Xóa sự kiện
│   │   ├── get_calendar/      # Xem lịch
│   │   └── update_calendar/   # Cập nhật sự kiện
│   └── gmail_features/        # Tính năng quản lý email
│       ├── search_emails/     # Tìm kiếm email
│       └── summarize_emails/  # Tóm tắt email
├── services/                  # Các dịch vụ bên ngoài
│   └── llm/                   # Dịch vụ mô hình ngôn ngữ lớn
└── utils/                     # Tiện ích và công cụ chung
    ├── default_text.py        # Văn bản mặc định cho chatbot
    └── helpers.py             # Hàm trợ giúp
```

### Các thành phần chính

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
   - Tích hợp mô hình ngôn ngữ lớn (LLM) - Gemini 2.0

4. **Database**: Lưu trữ lịch sử hội thoại và thông tin người dùng
   - Sử dụng MongoDB để lưu trữ dữ liệu

### Luồng xử lý Backend

1. Nhận yêu cầu từ người dùng qua giao diện chat
2. Chuyển yêu cầu trực tiếp đến agent_manager
3. Agent Manager phân tích ý định và chọn agent phù hợp (agent_calendar hoặc agent_gmail)
4. Trích xuất thông tin cần thiết
5. Thực hiện hành động tương ứng với API (Calendar, Gmail)
6. Tạo phản hồi cho người dùng
7. Lưu hội thoại vào cơ sở dữ liệu

## Frontend

Frontend của Neura là một giao diện web được xây dựng bằng HTML, CSS và JavaScript, kết hợp với Flask template.

### Cấu trúc Frontend

```plaintext
├── static/
│   ├── css/
│   │   └── style.css         # Style cho giao diện
│   ├── js/
│   │   └── chat.js           # Logic xử lý chat phía client
│   └── images/               # Hình ảnh và icons
└── templates/
    └── index.html            # Giao diện người dùng
```

### Các thành phần chính của Frontend

1. **Giao diện chat**:
   - Hiển thị lịch sử tin nhắn giữa người dùng và trợ lý
   - Hỗ trợ hiệu ứng đang nhập khi trợ lý đang xử lý

2. **Thanh bên Conversation**:
   - Hiển thị các cuộc hội thoại đã lưu
   - Cho phép tạo hội thoại mới
   - Cho phép xóa hội thoại

3. **Xử lý tương tác**:
   - Gửi yêu cầu người dùng đến server
   - Hiển thị phản hồi từ trợ lý
   - Nút thực hiện hành động (khi cần xác nhận)

### Tính năng chính của Frontend

1. **Chat liền mạch**: Giao diện chat thân thiện, hỗ trợ hiệu ứng gõ văn bản
2. **Quản lý hội thoại**: Lưu, tải và xóa các cuộc hội thoại
3. **Xác nhận hành động**: Nút thực hiện cho phép người dùng xác nhận trước khi thực hiện các tác vụ
4. **Định dạng tin nhắn**: Hỗ trợ hiển thị JSON và định dạng đặc biệt trong tin nhắn

## Tính năng chính của Neura

### Quản lý lịch (Calendar)

1. **Tạo sự kiện**: Tạo các sự kiện mới trong lịch
   - Sự kiện thông thường hoặc cuộc họp
   - Hỗ trợ sự kiện lặp lại (hàng ngày, hàng tuần, hàng tháng)
   - Đặt thời gian bắt đầu, kết thúc, địa điểm và người tham gia

2. **Xóa sự kiện**: Xóa các sự kiện đã tạo
   - Xóa theo tên sự kiện
   - Xóa theo khoảng thời gian

3. **Cập nhật sự kiện**: Chỉnh sửa thông tin sự kiện
   - Thay đổi thời gian, địa điểm, người tham gia
   - Chỉnh sửa tiêu đề hoặc mô tả

4. **Xem lịch**: Truy vấn thông tin lịch
   - Xem sự kiện trong ngày/tuần/tháng
   - Tìm thời gian rảnh

### Quản lý email (Gmail)

1. **Tìm kiếm email**: Tìm kiếm email trong hộp thư
   - Tìm theo người gửi, chủ đề, nội dung
   - Tìm theo khoảng thời gian

2. **Tóm tắt email**: Tóm tắt nội dung email
   - Tạo tóm tắt ngắn gọn các email quan trọng
   - Trích xuất thông tin chính từ email dài

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

## Cài đặt và triển khai

### Yêu cầu hệ thống

- Python 3.10 hoặc cao hơn
- MongoDB
- Google API credentials (Calendar và Gmail)

### Cài đặt

1. Clone repository
2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
3. Cấu hình Google API credentials:
   - Đặt file `credentials.json` vào thư mục gốc
   - Cấu hình scope cho cả Calendar và Gmail API
4. Khởi động ứng dụng:
   ```bash
   python app.py
   ```

## Kết luận

Neura là một trợ lý cá nhân AI đa năng, không chỉ giúp quản lý lịch trình mà còn hỗ trợ xử lý email một cách thông minh. Hệ thống được thiết kế với kiến trúc module hóa rõ ràng, dễ dàng mở rộng thêm các tính năng mới trong tương lai.

Với khả năng xử lý ngôn ngữ tự nhiên từ Gemini 2.0, Neura hiểu yêu cầu của người dùng và thực hiện các thao tác phức tạp một cách đơn giản, mang lại trải nghiệm tương tác tự nhiên và hiệu quả, như đang trò chuyện với một trợ lý cá nhân thực sự.