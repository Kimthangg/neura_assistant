import os
from dotenv import load_dotenv
load_dotenv()
# Thay token bot của m vào đây
BOT_TOKEN = os.getenv('BOT_TOKEN')
from db import MongoDBManager
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Bot
# Avoid circular import by using lazy import
bot_summary_email = Bot(token=BOT_TOKEN)

# Initialize MongoDB Manager
db_manager = MongoDBManager()
def split_text(text, max_length=4096):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

async def handle_message(update, context):
    # Import here to avoid circular imports
    from .agent_manager import agent_manager_executor_func
    
    # Nhận tin nhắn từ người dùng
    text = update.message.text
    # Gửi phản hồi lại người dùng dựa trên id chat
    chat_id = update.effective_chat.id
    print(f"{chat_id}: {text}")
    # lấy lịch sử chat từ MongoDB
    history = db_manager.load_chat_history("conversation_telegram")
    history.append({"type": "user", "content": text})
    # Gọi hàm xử lý từ agent_manager_executor_func
    response = agent_manager_executor_func(text, history)
    history.append({"type": "user", "content": response})
    db_manager.save_chat_history(chat_id="conversation_telegram", chat_history=history, conversation_name="Telegram Conversation")
    # nếu quá 4096 kí tự thì chia nhỏ ra
    for chunk in split_text(response):
        await context.bot.send_message(
            chat_id=chat_id,
            text=chunk,
            parse_mode="HTML"
        )
chat_id = os.getenv('USER_ID_TELEGRAM')
async def reponse_task_schedule(task_name):
    # Import here to avoid circular imports
    # from .agent_gmail import agent_gmail_executor_func
    from .agent_manager import agent_manager_executor_func
    # summary_task = agent_gmail_executor_func(task_name)
    summary_task = agent_manager_executor_func(task_name)
    
    
    # Gửi HTML qua Telegram
    for chunk in split_text(summary_task):
        await bot_summary_email.send_message(
            chat_id=chat_id,
            text=chunk,
            parse_mode="HTML"
        )
        
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

import asyncio
def run_bot_polling():
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Run the bot in this loop
    app.run_polling()
