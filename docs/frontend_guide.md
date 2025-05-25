"""
# Neura - Tài liệu Hướng dẫn Giao diện

Tài liệu này mô tả chi tiết về cấu trúc, chức năng và cách sử dụng giao diện người dùng của ứng dụng Neura - Trợ lý quản lý lịch.

## 1. Tổng quan

Giao diện Neura được xây dựng với:
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Ngôn ngữ**: HTML, CSS và JavaScript

Giao diện gồm hai thành phần chính:
- **Templates (index.html)**: Cấu trúc HTML và CSS
- **JavaScript (chat.js)**: Xử lý tương tác và gọi API

## 2. Cấu trúc giao diện

### 2.1 Thanh sidebar (bên trái)
- Logo và tiêu đề ứng dụng
- Nút tạo hội thoại mới
- Danh sách lịch sử hội thoại
- Hiển thị ID người dùng hiện tại

### 2.2 Khu vực chat (bên phải)
- Nút toggle sidebar
- Khung hiển thị tin nhắn
- Khu vực thông báo và nút thực thi lệnh
- Khu vực nhập và gửi tin nhắn

## 3. Các thành phần HTML chính

| ID | Mô tả |
| --- | --- |
| `sidebar` | Thanh bên chứa danh sách hội thoại |
| `conversation-list` | Danh sách các cuộc hội thoại |
| `chat-history` | Khung hiển thị tin nhắn |
| `message-input` | Ô nhập tin nhắn |
| `send-button` | Nút gửi tin nhắn |
| `new-chat-btn` | Nút tạo hội thoại mới |
| `sidebar-toggle` | Nút ẩn/hiện thanh bên |
| `user-id` | Hiển thị ID người dùng hiện tại |
| `status-message` | Hiển thị thông báo trạng thái |

## 4. Các lớp CSS chính

| Class | Mô tả |
| --- | --- |
| `collapsed` | Trạng thái sidebar bị ẩn |
| `message` | Style chung cho tin nhắn |
| `user-message` | Style tin nhắn người dùng |
| `assistant-message` | Style tin nhắn trợ lý |
| `conversation-item` | Style item trong danh sách hội thoại |
| `current-conversation` | Đánh dấu hội thoại đang chọn |
| `typing-indicator` | Hiệu ứng đang nhập tin nhắn |

## 5. Các hàm JavaScript quan trọng

### 5.1 Quản lý Sidebar

```javascript
function toggleSidebar()
```
- **Mô tả**: Chuyển đổi trạng thái hiển thị của sidebar
- **Chức năng**: Thêm/xóa class 'collapsed', thay đổi icon, lưu trạng thái vào localStorage

### 5.2 Quản lý Tin nhắn

```javascript
function addMessage(type, content, simulateTyping = false)
```
- **Mô tả**: Thêm tin nhắn vào khung chat
- **Tham số**:
  - `type`: Loại tin nhắn ('user' hoặc 'assistant')
  - `content`: Nội dung tin nhắn
  - `simulateTyping`: Bật/tắt hiệu ứng gõ chữ

```javascript
function simulateTypingEffect(element, text)
```
- **Mô tả**: Tạo hiệu ứng gõ từng chữ
- **Tham số**: Element DOM và text cần hiển thị

```javascript
function showTypingIndicator() / removeTypingIndicator()
```
- **Mô tả**: Hiển thị/ẩn chỉ báo đang nhập tin nhắn

### 5.3 API Communication

```javascript
async function sendMessage()
```
- **Mô tả**: Gửi tin nhắn người dùng đến server và xử lý phản hồi
- **Endpoint**: `/chat` (POST)
- **Đầu vào (Request)**:
  ```json
  {
    "message": "Nội dung tin nhắn của người dùng"
  }  ```
- **Đầu ra (Response)**:
  ```json
  {
    "response": "Phản hồi từ trợ lý"
  }
  ```
- **Xử lý Frontend**:
  1. Hiển thị tin nhắn người dùng
  2. Hiển thị chỉ báo đang nhập
  3. Gọi API  4. Hiển thị phản hồi với hiệu ứng gõ

### 5.4 Quản lý Hội thoại

```javascript
async function createNewConversation()
```
- **Mô tả**: Tạo hội thoại mới
- **Endpoint**: `/new_conversation` (POST)
- **Đầu vào (Request)**: Không cần dữ liệu
- **Đầu ra (Response)**:
  ```json
  {
    "success": true/false,
    "user_id": "id_người_dùng_mới"
  }
  ```
- **Xử lý Frontend**:
  1. Xóa toàn bộ lịch sử chat hiện tại
  2. Ẩn nút thực thi
  3. Cập nhật ID người dùng hiện tại trong UI
  4. Cập nhật danh sách hội thoại

```javascript
async function loadConversation(userId)
```
- **Mô tả**: Tải hội thoại theo ID
- **Endpoint**: `/load_conversation/{userId}` (POST)
- **Đầu vào (Request)**:
  - userId: ID của hội thoại (truyền qua URL parameter)
- **Đầu ra (Response)**:
  ```json
  {
    "success": true/false,
    "chat_history": [
      {
        "type": "user/assistant",
        "content": "Nội dung tin nhắn"
      }
    ]
  }
  ```
- **Xử lý Frontend**:
  1. Xóa toàn bộ lịch sử chat hiện tại
  2. Hiển thị từng tin nhắn trong lịch sử chat
  3. Ẩn nút thực thi
  4. Cập nhật ID người dùng hiện tại trong UI
  5. Đánh dấu hội thoại đang chọn trong danh sách

```javascript
async function deleteConversation(userId)
```
- **Mô tả**: Xóa hội thoại theo ID
- **Endpoint**: `/delete_conversation/{userId}` (POST)
- **Đầu vào (Request)**:
  - userId: ID của hội thoại (truyền qua URL parameter)
- **Đầu ra (Response)**:
  ```json
  {
    "success": true/false,
    "message": "Thông báo kết quả"
  }
  ```
- **Xử lý Frontend**:
  1. Xác nhận người dùng có chắc muốn xóa
  2. Gọi API
  3. Nếu hội thoại xóa là hội thoại hiện tại, xóa lịch sử chat
  4. Cập nhật danh sách hội thoại

```javascript
async function updateConversationList()
```
- **Mô tả**: Cập nhật danh sách hội thoại
- **Endpoint**: `/get_conversations` (GET)
- **Đầu vào (Request)**: Không cần dữ liệu
- **Đầu ra (Response)**:
  ```json
  {
    "conversations": [
      {
        "user_id": "id_người_dùng",
        "conversation_name": "Tên hội thoại",
        "updated_at": "Thời gian cập nhật"
      }
    ]
  }
  ```
- **Xử lý Frontend**:
  1. Xóa danh sách hội thoại hiện tại
  2. Hiển thị danh sách hội thoại mới
  3. Đánh dấu hội thoại đang chọn
  4. Thêm event listeners cho các hành động click và xóa

## 6. Các sự kiện (Events)

| Sự kiện | Element | Hàm xử lý |
| --- | --- | --- |
| `click` | Nút gửi | `sendMessage()` |
| `keypress` (Enter) | Input | `sendMessage()` |
| `click` | Nút tạo hội thoại | `createNewConversation()` |
| `click` | Item hội thoại | `loadConversation()` |
| `click` | Nút xóa hội thoại | `deleteConversation()` |
| `click` | Nút toggle sidebar | `toggleSidebar()` |

## 7. API Endpoints

| Endpoint | Method | Mô tả |
| --- | --- | --- |
| `/chat` | POST | Gửi tin nhắn và nhận phản hồi |
| `/new_conversation` | POST | Tạo hội thoại mới |
| `/load_conversation/{userId}` | POST | Tải hội thoại |
| `/delete_conversation/{userId}` | POST | Xóa hội thoại |
| `/get_conversations` | GET | Lấy danh sách hội thoại |

## 8. Luồng dữ liệu giữa Frontend và Backend Flask

### 8.1 Luồng xử lý tin nhắn

1. **Frontend gửi tin nhắn đến Flask**:
   - Người dùng nhập và gửi tin nhắn
   - JavaScript gọi `/chat` với payload JSON chứa tin nhắn
   - Frontend hiển thị chỉ báo đang nhập

2. **Xử lý trong Flask**:
   - Route `/chat` nhận tin nhắn từ request
   - Flask chuyển tin nhắn đến module xử lý (thường là LLM)
   - Module xử lý phân tích ý định (intent classification)
   - Tạo phản hồi và quyết định có cần hiển thị nút thực thi không

3. **Flask trả về kết quả cho Frontend**:
   - Trả về phản hồi dạng JSON với nội dung và trạng thái nút thực thi
   - Frontend hiển thị phản hồi với hiệu ứng gõ chữ

### 8.2 Luồng thực thi hành động

1. **Frontend yêu cầu thực thi**:
   - Người dùng nhấn nút "Thực hiện"
   - JavaScript gọi `/execute` API

2. **Xử lý trong Flask**:
   - Flask lấy ngữ cảnh của hội thoại hiện tại (được lưu trong session)
   - Phân tích hành động cần thực hiện (thêm/xóa/sửa lịch)
   - Thực hiện hành động với Google Calendar API
   - Cập nhật cơ sở dữ liệu nếu cần

3. **Flask trả về kết quả cho Frontend**:
   - Trả về kết quả thực thi dạng JSON
   - Frontend hiển thị thông báo kết quả và cập nhật UI

### 8.3 Luồng quản lý hội thoại

1. **Tạo hội thoại mới**:
   - Frontend gọi `/new_conversation`
   - Flask tạo ID người dùng mới và session mới
   - Trả về ID người dùng mới
   - Frontend xóa lịch sử chat và cập nhật UI

2. **Tải hội thoại**:
   - Frontend gọi `/load_conversation/{userId}`
   - Flask tìm hội thoại trong cơ sở dữ liệu
   - Trả về toàn bộ lịch sử chat
   - Frontend hiển thị lại lịch sử chat

3. **Xóa hội thoại**:
   - Frontend gọi `/delete_conversation/{userId}`
   - Flask xóa hội thoại khỏi cơ sở dữ liệu
   - Trả về kết quả xóa
   - Frontend cập nhật danh sách hội thoại

## 9. Định dạng dữ liệu truyền nhận

### 9.1 Định dạng tin nhắn

**Frontend gửi đến Flask**:
```json
{
  "message": "Tạo lịch họp ngày mai lúc 10 giờ"
}
```

**Flask trả về Frontend**:
```json
{
  "response": "Tôi sẽ tạo lịch họp vào ngày 17/04/2025 lúc 10:00. Bạn có muốn thực hiện không?"
}
```

### 9.2 Định dạng lịch sử hội thoại

**Flask trả về Frontend khi tải hội thoại**:
```json
{
  "success": true,
  "chat_history": [
    {
      "type": "user",
      "content": "Tạo lịch họp ngày mai lúc 10 giờ"
    },
    {
      "type": "assistant",
      "content": "Tôi sẽ tạo lịch họp vào ngày 17/04/2025 lúc 10:00. Bạn có muốn thực hiện không?"
    },
    {
      "type": "user",
      "content": "Có"
    },
    {
      "type": "assistant",
      "content": "Đã tạo lịch họp thành công vào ngày 17/04/2025 lúc 10:00."
    }
  ]
}
```

## 10. Tính năng đặc biệt

1. **Hiệu ứng gõ chữ**: Tạo cảm giác trợ lý đang nhập từng chữ
2. **Chỉ báo đang nhập**: Hiển thị khi đang chờ phản hồi
3. **Responsive layout**: Tự thích ứng với kích thước màn hình
4. **Lưu trạng thái**: Giữ trạng thái sidebar qua các lần truy cập
5. **Quản lý hội thoại**: Tạo, tải và xóa hội thoại

## 11. Hướng dẫn mở rộng

### 11.1 Thêm tính năng mới
1. Thêm HTML vào index.html
2. Thêm CSS (nếu cần)
3. Thêm hàm JavaScript vào chat.js
4. Thêm event listener
5. Thêm tương ứng API endpoint vào Flask

### 11.2 Tùy chỉnh giao diện
1. Sửa đổi các biến CSS cho màu sắc
2. Thay đổi font chữ và kích thước
3. Điều chỉnh layout
4. Thay đổi biểu tượng bằng cách sử dụng Font Awesome
"""