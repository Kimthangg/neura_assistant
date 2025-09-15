import os
import sys
import uuid
from flask import Flask, jsonify, render_template, request, session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

# Import required modules from your project
from bot.agent.agent_manager import agent_manager_executor_func
from bot.agent.agent_gmail import agent_gmail_executor_func
from bot.agent.agent_calendar import agent_calendar_executor_func
from db import MongoDBManager

# Import helper functions
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

# --- Web UI Route ---
@app.route("/")
def index():
    """Render the main chat interface"""
    ensure_user_id()
    # Lấy ds hội thoại từ cơ sở dữ liệu
    conversation_list = db_manager.get_all_conversations()
    # Chuyển đổi định dạng thời gian về múi giờ Việt Nam
    conversation_list = format_timezone(conversation_list, "index")
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

# --- RESTful API Routes ---

# API Resource: Conversations
# --------------------------

# GET /api/conversations - Get all conversations
@app.route("/api/conversations", methods=["GET"])
def get_conversations():
    """Get the list of all conversations
    
    Returns:
        200 OK - List of conversations
    """
    conversations = db_manager.get_all_conversations()
    # Format the conversation timestamps to Vietnam timezone
    conversations = format_timezone(conversations)
    return jsonify({"data": conversations}), 200

# POST /api/conversations - Create a new conversation
@app.route("/api/conversations", methods=["POST"])
def create_conversation():
    """Create a new conversation
    
    Returns:
        201 Created - Newly created conversation ID
    """
    # Create new conversation with UUID
    new_conversation_id = str(uuid.uuid4())
    
    # Update session if this is current user's action
    if request.args.get("use_session", "true").lower() == "true":
        session["user_id"] = new_conversation_id
        session["conversation_name_set"] = False
        session.modified = True
        
        # Reset agents if needed
        agent_gmail_executor_func("", True)
        agent_calendar_executor_func("", True)
    
    # Return the new conversation ID
    return jsonify({
        "message": "Hội thoại mới đã được tạo",
        "data": {"id": new_conversation_id}
    }), 201

# GET /api/conversations/{id} - Get a specific conversation
@app.route("/api/conversations/<conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    """Get a specific conversation by ID
    
    Args:
        conversation_id: The ID of the conversation to retrieve
        
    Returns:
        200 OK - Conversation data
        404 Not Found - If conversation doesn't exist
    """
    # Load chat history from database
    chat_history = db_manager.load_chat_history(conversation_id)
    
    # Check if conversation exists
    if not chat_history:
        return jsonify({"error": "Không tìm thấy hội thoại"}), 404
    
    # Format chat history if requested
    format_as = request.args.get("format", "json")
    if format_as == "html":
        chat_history_formatted = convert_chat_history_to_html(chat_history)
        return jsonify({"data": chat_history_formatted}), 200
    
    # Return JSON by default
    return jsonify({"data": chat_history}), 200

# DELETE /api/conversations/{id} - Delete a conversation
@app.route("/api/conversations/<conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    """Delete a conversation by ID
    
    Args:
        conversation_id: The ID of the conversation to delete
        
    Returns:
        204 No Content - If successfully deleted
        404 Not Found - If conversation doesn't exist
    """
    # Delete conversation from database
    success = db_manager.delete_chat_history(conversation_id)
    
    if success:
        # If deleted the current conversation, create a new one for the session
        if conversation_id == session.get("user_id") and request.args.get("create_new", "true").lower() == "true":
            session["user_id"] = str(uuid.uuid4())
            session["conversation_name_set"] = False
            session.modified = True
            
        # Return 204 No Content on success (RESTful standard for successful DELETE)
        return "", 204
    else:
        # Return 404 Not Found if conversation doesn't exist
        return jsonify({"error": "Không tìm thấy hội thoại"}), 404

# PUT /api/conversations/{id}/active - Make a conversation active in the session
@app.route("/api/conversations/<conversation_id>/active", methods=["PUT"])
def set_active_conversation(conversation_id):
    """Make a conversation active in the current session
    
    Args:
        conversation_id: The ID of the conversation to make active
        
    Returns:
        200 OK - If conversation set as active
        404 Not Found - If conversation doesn't exist
    """
    # Check if already active
    if conversation_id == session.get("user_id"):
        return jsonify({"message": "Hội thoại này đã đang hoạt động"}), 200
        
    # Load chat history to verify conversation exists
    chat_history = db_manager.load_chat_history(conversation_id)
    
    if not chat_history:
        return jsonify({"error": "Không tìm thấy hội thoại"}), 404
    
    # Update session
    session["user_id"] = conversation_id
    session["conversation_name_set"] = True
    session.modified = True
    
    # Return success
    return jsonify({"message": "Đã chuyển sang hội thoại này"}), 200

# API Resource: Messages
# ---------------------

# POST /api/conversations/{id}/messages - Add a message to a conversation
@app.route("/api/conversations/<conversation_id>/messages", methods=["POST"])
def add_message(conversation_id):
    """Add a message to a conversation and get AI response
    
    Args:
        conversation_id: The ID of the conversation to add message to
        
    Body (JSON):
        message: The user message text
        
    Returns:
        201 Created - New message and AI response
        400 Bad Request - If message is missing
        404 Not Found - If conversation doesn't exist
    """
    # Get message from request
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Thiếu nội dung tin nhắn"}), 400
    
    user_message = data["message"]
    
    # Check if we should use session conversation instead
    use_session_id = request.args.get("use_session", "false").lower() == "true"
    actual_id = session.get("user_id") if use_session_id else conversation_id
    
    # Load chat history
    chat_history = db_manager.load_chat_history(actual_id)
    
    # If no history and not creating new, return 404
    if not chat_history and not request.args.get("create_if_missing", "false").lower() == "true":
        return jsonify({"error": "Không tìm thấy hội thoại"}), 404
    
    # Add user message to history
    chat_history.append({"type": "user", "content": user_message})
    
    # Process with LLM
    ai_response = agent_manager_executor_func(user_message, chat_history)
    
    # Add AI response to history
    chat_history.append({"type": "assistant", "content": ai_response})
    
    # Set conversation name if first message
    if not session.get("conversation_name_set", False) and use_session_id:
        conversation_name = user_message[:50]
        if len(user_message) >= 50:
            conversation_name += "..."
        session["conversation_name_set"] = True
        db_manager.save_chat_history(actual_id, chat_history, conversation_name)
    else:
        db_manager.save_chat_history(actual_id, chat_history)
    
    # Mark session as modified
    if use_session_id:
        session.modified = True
    
    # Format response if requested
    import markdown2
    format_as = request.args.get("format", "json")
    if format_as == "html":
        ai_response_formatted = markdown2.markdown(ai_response.replace("\n", "<br>"), extras=["autolink"])
    else:
        ai_response_formatted = ai_response
    
    # Return the new message data
    return jsonify({
        "data": {
            "user_message": user_message,
            "ai_response": ai_response_formatted
        }
    }), 201

# --- Server Startup ---

def run_flask_app():
    """Run the Flask application"""
    app.run(
        # host='0.0.0.0',  # Cho phép truy cập từ bên ngoài nếu cần
        port=5000,  # Port mặc định
        # debug=True,  # Bật debug mode khi cần
        threaded=True,  # Enable threading to handle multiple requests
    )

if __name__ == "__main__":
    app.run(
        # host='0.0.0.0',
        port=5000,
        # debug=True,
        threaded=True,
    )
