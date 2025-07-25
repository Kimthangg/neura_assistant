"""
Script to run both the Telegram bot and Flask web application simultaneously.
Run this file to start both applications.
"""

import os
import threading
import sys
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# Import the run_both_applications function from the bot_telegram module
from app.app import run_flask_app
from bot.agent.bot_telegram import run_telegram_bot

# Hàm chính để chạy cả hai ứng dụng
def run_both_applications():
    # Tạo thread cho Telegram bot
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.daemon = True  # Đảm bảo thread sẽ kết thúc khi chương trình chính kết thúc
    
    # Tạo thread cho Flask app
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True  # Đảm bảo thread sẽ kết thúc khi chương trình chính kết thúc
    
    # Bắt đầu các thread
    telegram_thread.start()
    flask_thread.start()
    
    # Chờ thread Telegram kết thúc (điều này chỉ xảy ra khi có KeyboardInterrupt)
    try:
        telegram_thread.join()
    except KeyboardInterrupt:
        print("Shutting down...")
if __name__ == "__main__":
    print("Starting both Telegram bot and Flask web application...")
    print("Press Ctrl+C to stop both applications")
    run_both_applications()
