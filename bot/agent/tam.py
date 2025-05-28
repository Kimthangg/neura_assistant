from ..agent_intent import intent_model
 
def handle_tam(query):
    """
    Xử lý truy vấn với agent tam (tạm thời) để trả về kết quả.
    
    Parameters:
        query (str): Truy vấn đầu vào từ người dùng.
        history_chat (list): Lịch sử trò chuyện dạng list (dicts hoặc messages).
    
    Returns:
        str: Kết quả từ agent tam hoặc thông báo lỗi.
    """
    try:
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