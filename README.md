# Neura - Trợ lý quản lý lịch thông minh

Neura là một ứng dụng trợ lý ảo giúp người dùng quản lý lịch và sự kiện thông qua giao diện chat trực quan. Ứng dụng sử dụng kỹ thuật xử lý ngôn ngữ tự nhiên (NLP) để hiểu yêu cầu của người dùng và thực hiện các thao tác với Google Calendar.

## Tổng quan hệ thống

Hệ thống Neura được chia thành hai phần chính:

1. **Backend**: Xử lý logic nghiệp vụ, tương tác với API bên ngoài và xử lý ngôn ngữ tự nhiên
2. **Frontend**: Giao diện người dùng dạng chat trực quan

```
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
│               │  HTTP Requests                  │          │          │  │
│               │                                 │          │          │  │
├───────────────┼─────────────────────────────────┼──────────┼──────────┤  │
│               │                                 │          │          │  │
│               ▼                                 │          │          │  │
│     ┌───────────────────┐                       │          │          │  │
│     │                   │                       │          │          │  │
│     │   Flask Server    │◄──────────────────────┘          │          │  │
│     │   (app/app.py)    │                                  │          │  │
│     │                   │                                  │          │  │
│     └────────┬──────────┘                                  │          │  │
│              │                                             │          │  │
│              │                                             │          │  │
│              ▼                                             │          │  │
│    ┌────────────────────┐                                  │          │  │
│    │                    │                                  │          │  │
│    │ Bot Module         │                                  │          │  │
│    │ ┌────────────────┐ │         ┌─────────────────┐     │          │  │
│    │ │ Agent Intent   │ │         │                 │     │          │  │
│    │ │ (Classification)│ │         │  LLM Service   │     │          │  │
│    │ └────────────────┘ │◄────────┤  (Gemini 2.0)  │     │          │  │
│    │ ┌────────────────┐ │         │                 │     │          │  │
│    │ │Agent Extraction│ │         └─────────────────┘     │          │  │
│    │ │(Data Extraction)│ │                                │          │  │
│    │ └────────────────┘ │                                 │          │  │
│    │ ┌────────────────┐ │                                 │          │  │
│    │ │    Handler     │ │                                 │          │  │
│    │ │(Message Flow)  │◄├─────────────────────────────────┘          │  │
│    │ └────────────────┘ │                                            │  │
│    └──────────┬─────────┘                                            │  │
│               │                                                      │  │
│               │                                                      │  │
│               ▼                                                      │  │
│     ┌───────────────────┐                                            │  │
│     │                   │                                            │  │
│     │     MongoDB       │                                            │  │
│     │    Database       │                                            │  │
│     │                   │                                            │  │
│     └───────────────────┘                                            │  │
│                                                                      │  │
└──────────────────────────────────────────────────────────────────────┘
```

## Backend

Backend của Neura được xây dựng bằng Python với Flask framework và tích hợp các công nghệ sau:

### Cấu trúc Backend

```
├── app.py                     # Điểm khởi đầu ứng dụng Flask 
├── bot/                       # Các module xử lý logic chatbot
│   ├── agent_extraction/      # Trích xuất thông tin từ tin nhắn người dùng
│   │   ├── create_event/      # Xử lý tạo sự kiện
│   │   ├── delete_event/      # Xử lý xóa sự kiện
│   │   ├── get_event/         # Xử lý lấy thông tin sự kiện
│   │   └── update_event/      # Xử lý cập nhật sự kiện
│   ├── agent_intent/          # Phân loại ý định người dùng
│   └── handler/               # Xử lý luồng tin nhắn
├── config/                    # Cấu hình hệ thống
│   ├── calendar.py            # Cấu hình Google Calendar API
│   ├── environment.py         # Biến môi trường
│   └── mongodb.py             # Cấu hình MongoDB
├── features/                  # Các tính năng chính của ứng dụng
│   ├── create_calendar/       # Tính năng tạo sự kiện
│   ├── delete_calendar/       # Tính năng xóa sự kiện
│   ├── get_calendar/          # Tính năng xem lịch
│   └── update_calendar/       # Tính năng cập nhật sự kiện
├── services/                  # Các dịch vụ bên ngoài
│   └── llm/                   # Dịch vụ mô hình ngôn ngữ lớn
└── utils/                     # Tiện ích và công cụ chung
    ├── db_manager.py          # Quản lý cơ sở dữ liệu
    └── helpers.py             # Hàm trợ giúp
```

### Các thành phần chính

1. **Agent Intent**: Sử dụng NLP để phân loại ý định người dùng (tạo, xóa, cập nhật, xem sự kiện...)
   - Phân tích văn bản đầu vào từ người dùng
   - Phân loại thành các loại ý định cụ thể (create_normal_event, update_event, delete_event, get_freetime, v.v.)
   - Đánh giá độ tin cậy của việc phân loại

2. **Agent Extraction**: Trích xuất thông tin quan trọng từ yêu cầu của người dùng
   - Phân tích và trích xuất ngày giờ (datetime_extraction.py)
   - Xác định tính lặp lại của sự kiện
   - Xác thực dữ liệu đầu vào (validate.py)

3. **Handler**: Quản lý luồng tin nhắn và tương tác
   - Xử lý tin nhắn đầu vào (message.py)
   - Tạo phản hồi (gen.py)

4. **Services**: Kết nối với các dịch vụ bên ngoài
   - Tương tác với Google Calendar API
   - Tích hợp mô hình ngôn ngữ lớn (LLM)

5. **Database**: Lưu trữ lịch sử hội thoại và thông tin người dùng
   - Sử dụng MongoDB để lưu trữ dữ liệu

### Luồng xử lý Backend

1. Nhận yêu cầu từ người dùng qua giao diện chat
2. Phân tích ý định (agent_intent)
3. Trích xuất thông tin cần thiết (agent_extraction)
4. Thực hiện hành động tương ứng với API Google Calendar
5. Tạo phản hồi cho người dùng
6. Lưu hội thoại vào cơ sở dữ liệu

## Frontend

Frontend của Neura là một giao diện web được xây dựng bằng HTML, CSS và JavaScript, kết hợp với Flask template.

### Cấu trúc Frontend

```
├── static/
│   ├── js/
│   │   └── chat.js           # Logic xử lý chat phía client
│   └── css/                  # (Nếu có file CSS riêng)
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
3. **Xác nhận hành động**: Nút thực hiện cho phép người dùng xác nhận trước khi tạo/cập nhật/xóa sự kiện
4. **Định dạng tin nhắn**: Hỗ trợ hiển thị JSON và định dạng đặc biệt trong tin nhắn

## Luồng hoạt động của hệ thống

1. **Người dùng nhập yêu cầu**:
   - Ví dụ: "Tạo lịch họp với team vào 2h chiều mai tại phòng 301"

2. **Frontend gửi yêu cầu tới Backend**:
   - Gửi POST request đến endpoint `/chat`
   - Hiển thị hiệu ứng "đang nhập" cho người dùng

3. **Backend xử lý yêu cầu**:
   - app.py nhận yêu cầu và gọi hàm `gen_llm()`
   - Phân loại ý định (agent_intent)
   - Trích xuất thông tin (agent_extraction)
   - Tạo phản hồi dựa trên ý định đã phân loại

4. **Phản hồi đến người dùng**:
   - Backend trả về JSON chứa phản hồi và trạng thái
   - Frontend hiển thị phản hồi với hiệu ứng gõ văn bản
   - Nếu cần xác nhận hành động, hiển thị nút "Thực hiện"

5. **Thực hiện hành động (nếu có)**:
   - Khi người dùng nhấn "Thực hiện", gửi request đến `/execute`
   - Backend thực hiện hành động với Google Calendar API
   - Trả về kết quả thành công hoặc thất bại

6. **Lưu hội thoại**:
   - Lưu lịch sử hội thoại vào MongoDB
   - Cập nhật danh sách hội thoại trong giao diện

## Cài đặt và triển khai

### Yêu cầu hệ thống

- Python 3.10 hoặc cao hơn
- MongoDB
- Google Calendar API credentials

### Cài đặt

1. Clone repository
2. Cài đặt các thư viện phụ thuộc:
   ```
   pip install -r requirements.txt
   ```
3. Cấu hình Google Calendar API credentials:
   - Đặt file `credentials.json` vào thư mục gốc
4. Khởi động ứng dụng:
   ```
   python app.py
   ```

## Kết luận

Neura là một trợ lý ảo thông minh giúp người dùng quản lý lịch trình một cách hiệu quả. Hệ thống được thiết kế với kiến trúc rõ ràng, phân tách giữa backend và frontend, giúp dễ dàng bảo trì và mở rộng trong tương lai.

Với khả năng xử lý ngôn ngữ tự nhiên, Neura có thể hiểu yêu cầu của người dùng và thực hiện các thao tác với Google Calendar một cách trực quan, giống như đang trò chuyện với một trợ lý thực sự.