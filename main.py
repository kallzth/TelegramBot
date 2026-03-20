import logging
import datetime  # Needed for the scheduler
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.ext import InlineQueryHandler # Add this import
from bot.commands.inline import inline_query_handler # Add this import
# Import your handlers
from bot.core.config import TELEGRAM_BOT_TOKEN
from bot.commands.start import start_handler
from bot.commands.summarize import summarize_handler
from bot.commands.prompt import prompt_handler
from bot.commands.eng_tools import git_handler, debug_handler
from bot.commands.kb_handler import save_handler, ask_handler, clear_kb_handler
from bot.commands.image_handler import image_message_handler
# Logging setup 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Define the automated task
async def morning_reminder(context):
    # We will replace "YOUR_CHAT_ID" with your actual ID below
    await context.bot.send_message(
        chat_id="536205799", 
        text="☀️ **Morning Engineer!**\nTime to check your PRs and set your daily goal."
    )

if __name__ == '__main__':
    # Build application with job_queue enabled [cite: 7]
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Schedule the morning briefing 
    job_queue = application.job_queue
    job_queue.run_daily(morning_reminder, time=datetime.time(hour=9, minute=0))

    # 1. Register Slash Commands [cite: 7]
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('summarize', summarize_handler))
    application.add_handler(CommandHandler('prompt', prompt_handler))
    application.add_handler(CommandHandler('git', git_handler))
    application.add_handler(CommandHandler('debug', debug_handler))
    application.add_handler(InlineQueryHandler(inline_query_handler))
    # Register Memory Commands
    application.add_handler(CommandHandler('save', save_handler))
    application.add_handler(CommandHandler('ask', ask_handler))
    application.add_handler(CommandHandler('clear_kb', clear_kb_handler))

    # 2. Register Button Menu Handlers 
    application.add_handler(MessageHandler(filters.Text("📝 Summarize"), summarize_handler))
    application.add_handler(MessageHandler(filters.Text("🏗️ Prompt Gen"), prompt_handler))
    application.add_handler(MessageHandler(filters.Text("💾 Git Commit"), git_handler))
    application.add_handler(MessageHandler(filters.Text("🔍 Debug Log"), debug_handler))
    # Register Image Handler
    application.add_handler(MessageHandler(filters.PHOTO, image_message_handler))
    
    print("Bot is polling with Scheduler & Advanced UX enabled...")
    application.run_polling()