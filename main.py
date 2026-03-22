import sys
import os
from dotenv import load_dotenv 

# 1. PATH FIX FIRST (So Python can find the 'bot' folder)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. LOAD ENV VARIABLES
load_dotenv() 

import logging
import datetime
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, InlineQueryHandler

# 3. NOW IMPORT BOT HANDLERS (After path is fixed)
from bot.core.config import TELEGRAM_BOT_TOKEN
from bot.commands.start import start_handler
from bot.commands.summarize import summarize_handler
from bot.commands.prompt import prompt_handler
from bot.commands.eng_tools import git_handler, debug_handler
from bot.commands.kb_handler import save_handler, ask_handler, clear_kb_handler
from bot.commands.image_handler import image_message_handler
from bot.commands.inline import inline_query_handler

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Keep-alive server
app = Flask('')
@app.route('/')
def home(): return "Bot is awake!"

def run(): app.run(host='0.0.0.0', port=8080)

# Automated task
async def morning_reminder(context):
    await context.bot.send_message(
        chat_id="536205799", 
        text="☀️ **Morning Engineer!**\nTime to check your PRs and set your daily goal."
    )

if __name__ == '__main__':
    # 4. START KEEP-ALIVE SERVER
    Thread(target=run).start()
    print("🌍 Keep-alive server started on port 8080...")

    # 5. BUILD APPLICATION
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # 6. SCHEDULE TASKS
    job_queue = application.job_queue
    job_queue.run_daily(morning_reminder, time=datetime.time(hour=9, minute=0))

    # 7. REGISTER HANDLERS
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('summarize', summarize_handler))
    application.add_handler(CommandHandler('prompt', prompt_handler))
    application.add_handler(CommandHandler('git', git_handler))
    application.add_handler(CommandHandler('debug', debug_handler))
    application.add_handler(InlineQueryHandler(inline_query_handler))
    
    application.add_handler(CommandHandler('save', save_handler))
    application.add_handler(CommandHandler('ask', ask_handler))
    application.add_handler(CommandHandler('clear_kb', clear_kb_handler))

    application.add_handler(MessageHandler(filters.Text("📝 Summarize"), summarize_handler))
    application.add_handler(MessageHandler(filters.Text("🏗️ Prompt Gen"), prompt_handler))
    application.add_handler(MessageHandler(filters.Text("💾 Git Commit"), git_handler))
    application.add_handler(MessageHandler(filters.Text("🔍 Debug Log"), debug_handler))
    application.add_handler(MessageHandler(filters.PHOTO, image_message_handler))
    
    print("🤖 Bot is polling with Scheduler & Advanced UX enabled...")
    application.run_polling()