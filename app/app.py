
import os
import sys
import uuid

from flask import Flask, jsonify, render_template, request, session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

# Import required modules from your project
from bot import agent_manager_executor_func, agent_gmail_executor_func, agent_calendar_executor_func
from db import MongoDBManager

#Import hàm helper
from utils import format_timezone, convert_chat_history_to_html

# --- Initialization ---
app = Flask(__name__)
# Set a secret key for session management
app.secret_key = os.urandom(24)

# Initialize MongoDB Manager
db_manager = MongoDBManager()

# --- Helper Functions ---
def ensure_user_id():
    """Ensure user_id exists in session"""
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
        session["conversation_name_set"] = False

# --- Flask Routes ---
@app.route("/")
def index():
    """Render the main chat interface"""
    ensure_user_id()
    # Lấy ds hội thoại từ cơ sở dữ liệu
    conversation_list = db_manager.get_all_conversations()
    # Chuyển đổi định dạng thời gian về múi giờ Việt Nam
    conversation_list = format_timezone(conversation_list,"index")
      # Get current chat history from database instead of session
    current_chat_history = db_manager.load_chat_history(session["user_id"])
    
    # Convert chat history messages to HTML using markdown2
    chat_history_html = convert_chat_history_to_html(current_chat_history)
    
    return render_template(
        "index.html",
        chat_history=chat_history_html,
        conversation_list=conversation_list,
        current_chat_id=session.get("user_id", ""),
    )

import markdown2
@app.route("/chat", methods=["POST"])
def chat():
    """Handle incoming chat messages"""
    ensure_user_id()

    # Get user message from request
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    # Load chat history from database instead of session
    chat_history = db_manager.load_chat_history(session["user_id"])
    chat_history.append({"type": "user", "content": user_message})
    
    # Process message with LLM - Truyền chat_history từ database vào gen_llm
    response = agent_manager_executor_func(user_message, chat_history)
    
    # Update chat history in database
    chat_history.append({"type": "assistant", "content": response})

    # Set conversation name if this is the first message
    if not session.get("conversation_name_set", False):
        conversation_name = user_message[:50]
        if len(user_message) >= 50:
            conversation_name += "..."
        session["conversation_name_set"] = True
        db_manager.save_chat_history(
            session["user_id"], chat_history, conversation_name
        )
    else:
        db_manager.save_chat_history(session["user_id"], chat_history)    # Mark session as modified to ensure it's saved
    session.modified = True
    response_html = markdown2.markdown(response.replace("\n", "<br>"), extras=["autolink"])  

    return jsonify({"response": response_html})


@app.route("/new_conversation", methods=["POST"])
def new_conversation():
    """Start a new conversation"""

    # Create new conversation
    session["user_id"] = str(uuid.uuid4())
    session["conversation_name_set"] = False
    session.modified = True
    
    agent_gmail_executor_func("",True)
    agent_calendar_executor_func("",True)

    return jsonify({"success": True, "message": "Đã bắt đầu hội thoại mới!"})


@app.route("/load_conversation/<user_id>", methods=["POST"])
def load_conversation(user_id):
    """Load a saved conversation"""
    if user_id == session.get("user_id"):
        return jsonify({"success": False, "message": "Đây là hội thoại hiện tại"})    # Load chat history from database
    chat_history = db_manager.load_chat_history(user_id)

    # Update session
    session["user_id"] = user_id
    session["conversation_name_set"] = True
    session.modified = True
    
    # Convert chat history messages to HTML using markdown2
    chat_history_html = convert_chat_history_to_html(chat_history)
    
    return jsonify({"success": True, "chat_history": chat_history_html})


@app.route("/delete_conversation/<user_id>", methods=["POST"])
def delete_conversation(user_id):
    """Delete a conversation"""
    success = db_manager.delete_chat_history(user_id)

    if success:
        # If deleted the current conversation, create a new one
        if user_id == session.get("user_id"):
            session["user_id"] = str(uuid.uuid4())
            session["conversation_name_set"] = False
            session.modified = True

        return jsonify({"success": True, "message": "Đã xóa hội thoại thành công!"})
    else:
        return jsonify({"success": False, "message": "Có lỗi khi xóa hội thoại!"})


@app.route("/get_conversations", methods=["GET"])
def get_conversations():
    """Get the list of saved conversations"""
    conversations = db_manager.get_all_conversations()
    # Format the conversation timestamps to Vietnam timezone
    conversations = format_timezone(conversations)
    return jsonify({"conversations": conversations})


if __name__ == "__main__":
    app.run(
        # host='0.0.0.0',  # Cho phép truy cập từ bên ngoài nếu cần
        port=5000,  # Hoặc bất kỳ port nào Cậu muốn
        # debug=True,  # Bật debug mode, auto-reload khi thay code
    )
