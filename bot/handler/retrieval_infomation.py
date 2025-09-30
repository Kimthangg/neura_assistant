import uuid
from db import MongoDBManager
db_manager = MongoDBManager()
def retrieval_info(user_query):
    """
    Truy xuất thông tin liên quan đến truy vấn của người dùng.
    Hàm này sử dụng tìm kiếm vector để tìm các thông tin của người dùng hoặc email có nội dung liên quan 
    đến truy vấn được cung cấp.
    Tham số:
        user_query (str): Truy vấn văn bản của người dùng để tìm kiếm thông tin liên quan.
    Trả về:
        list hoặc str: Danh sách các email liên quan nếu tìm thấy, hoặc thông báo lỗi 
        nếu không tìm thấy dữ liệu phù hợp.
    """
    data = db_manager.search_info_by_vector(query_text=user_query)
    if data:
        return data
    else:
        return "Không tìm thấy dữ liệu có liên quan cho truy vấn đã cho hãy sử dụng công cụ (Tool) khác"
def save_information(information):
    """
    Lưu trữ thông tin vào cơ sở dữ liệu.
    Tham số:
        information (str): Thông tin cần lưu trữ.
    Trả về:
        bool: True nếu lưu trữ thành công, False nếu có lỗi.
    """
    id = uuid.uuid4().hex[:16]
    data_user = [{
        "id": id,
        "personal_data": information
    }]
    result = db_manager.save_info(emails=data_user)
    return result
