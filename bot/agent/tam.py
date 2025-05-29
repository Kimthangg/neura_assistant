from ..agent_intent import intent_model
import os, json
def handle_tam(query):
    """
    Xử lý truy vấn với agent tam (tạm thời) để trả về kết quả.
    
    Parameters:
        query (str): Truy vấn đầu vào từ người dùng.
        history_chat (list): Lịch sử trò chuyện dạng list (dicts hoặc messages).
    
    Returns:
        str: Kết quả từ agent tam hoặc thông báo lỗi.
    """
    last_parameters_path = "last_parameter.json"

    if os.path.exists(last_parameters_path):
        try:
            with open(last_parameters_path, 'r', encoding='utf-8') as file:
                last_params = json.load(file)
                print("Last intent loaded:", last_params.get('intent'))
            # Gắn thông tin từ file vào query
                intent = last_params.get('intent')
        except (json.JSONDecodeError, FileNotFoundError):
            # Nếu có lỗi đọc file, tiếp tục với query gốc
            intent = None
    try:
        if not intent:
            # Thực hiện truy vấn với intent_model
            intent = intent_model(query)
        print(f"Xác định ý định: {intent}")
        if intent.get('intent') == 'calendar':
            from .agent_calendar import agent_calendar_executor_func
            return agent_calendar_executor_func(query)
        elif intent.get('intent') == 'gmail':
            from .agent_gmail import agent_gmail_executor_func
            return agent_gmail_executor_func(query)
        # elif intent == 'normal_message':
        #     from .agent_normal_message import agent_normal_message_executor_func
        #     return agent_normal_message_executor_func(query, history_chat)
    except Exception as e:
        return f"Đã xảy ra lỗi khi xử lý truy vấn: {str(e)}"