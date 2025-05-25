"""
Script để test timezone trong database
"""
import datetime
import pytz
from db.db_manager import MongoDBManager

def test_timezone():
    """Test timezone handling trong database"""
    
    # Khởi tạo manager
    db_manager = MongoDBManager()
    
    # Hiển thị các timezone hiện tại
    print("=== KIỂM TRA TIMEZONE ===")
    
    # UTC time
    utc_now = datetime.datetime.utcnow()
    print(f"UTC time (utcnow): {utc_now}")
    
    # Local time
    local_now = datetime.datetime.now()
    print(f"Local time (now): {local_now}")
    
    # Vietnam timezone
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_now = datetime.datetime.now(vietnam_tz)
    print(f"Vietnam time (with timezone): {vietnam_now}")
    
    # UTC với timezone aware
    utc_tz = pytz.UTC
    utc_aware = datetime.datetime.now(utc_tz)
    print(f"UTC time (timezone aware): {utc_aware}")
    
    print("\n=== TEST LƯU VÀ ĐỌC DATABASE ===")
    
    # Test save với conversation name có timestamp
    test_chat_id = "test_timezone_123"
    test_history = [
        {"type": "user", "content": "Test timezone message"},
        {"type": "assistant", "content": "Response to timezone test"}
    ]
    
    # Lưu vào DB
    success = db_manager.save_chat_history(test_chat_id, test_history)
    print(f"Save result: {success}")
    
    # Đọc từ DB
    if success:
        # Lấy raw data từ MongoDB để xem timestamp
        result = db_manager.collection.find_one({"chat_id": test_chat_id})
        if result:
            print(f"Created at: {result.get('created_at')}")
            print(f"Updated at: {result.get('updated_at')}")
            print(f"Conversation name: {result.get('conversation_name')}")
            
            # So sánh với thời gian hiện tại
            created_time = result.get('created_at')
            if created_time:
                print(f"Created time type: {type(created_time)}")
                print(f"Created time timezone: {created_time.tzinfo}")
                
                # Chuyển đổi sang Vietnam timezone nếu cần
                if created_time.tzinfo is None:
                    # Nếu naive datetime, coi như UTC
                    created_utc = pytz.UTC.localize(created_time)
                else:
                    created_utc = created_time
                    
                created_vietnam = created_utc.astimezone(vietnam_tz)
                print(f"Created time in Vietnam: {created_vietnam}")
    
    # Dọn dẹp
    db_manager.delete_chat_history(test_chat_id)
    db_manager.close()

if __name__ == "__main__":
    test_timezone()
