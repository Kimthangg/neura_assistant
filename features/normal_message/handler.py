from utils import *


def process_normal_message(func_data):
    """
    Function to process normal messages

    Parameters:
    func_data: Data containing message details

    Returns:
    dict: Response data
    """
    message_data = parse_to_dict(func_data)
    print("message_data", message_data)

    # Process the message based on its content
    response = {
        "message": "Đã nhận được tin nhắn",
        "content": message_data.get("content", ""),
    }

    return response
