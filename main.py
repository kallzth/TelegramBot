import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

import logging

from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, InlineQueryHandler

from bot.core.config import TELEGRAM_BOT_TOKEN
from bot.commands.start import start_handler
from bot.commands.summarize import summarize_handler
from bot.commands.prompt import prompt_handler
from bot.commands.eng_tools import git_handler, debug_handler
from bot.commands.kb_handler import save_handler, ask_handler, clear_kb_handler
from bot.commands.image_handler import image_message_handler
from bot.commands.inline import inline_query_handler
from bot.commands.tip import tip_handler
from bot.commands.explain import explain_handler
from bot.commands.todo import todo_handler
from bot.commands.plan import plan_handler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Keep-alive server
app = Flask('')

@app.route('/')
def home(): return "Bot is awake!"

def run(): app.run(host='0.0.0.0', port=8080)

# ✅ FIX: Use Africa/Addis_Ababa timezone (UTC+3)
ADDIS_TZ = pytz.timezone("Africa/Addis_Ababa")


async def fallback_handler(update: Update, context):
    text = update.message.text.strip()
    lower = text.lower()
    user_name = update.message.from_user.first_name
    greetings = ["hi", "hello", "hey", "hiya", "howdy", "sup", "yo"]

    if any(lower == g for g in greetings):
        await update.message.reply_text(
            f"👋 Hey {user_name}! I'm your Engineering Assistant Bot!\n\n"
            "Here's what I can do for you:\n"
            "📝 /summarize — Summarize any text\n"
            "🏗️ /prompt — Generate AI prompts\n"
            "💾 /git — Write git commit messages\n"
            "🔍 /debug — Analyze error logs\n"
            "💡 /tip — Daily engineering tip\n"
            "🧠 /explain — Explain any concept or code\n"
            "📋 /todo — Manage your task list\n"
            "🗓️ /plan — Format your daily goals\n"
            "💾 /save — Save notes to knowledge base\n"
            "❓ /ask — Ask from your knowledge base\n\n"
            "Or use the buttons below! 👇"
        )

    elif "\n" in text or update.message.reply_to_message:
        goals = [g.strip() for g in text.split("\n") if g.strip()]
        if len(goals) >= 2:
            emojis = ["🥇", "🥈", "🥉", "🎯", "⭐", "💡", "🔥", "✅"]
            formatted = f"🗓 {user_name.upper()}'S DAILY BATTLE PLAN\n"
            formatted += "━━━━━━━━━━━━━━━━━━━━\n\n"
            for i, goal in enumerate(goals):
                emoji = emojis[i] if i < len(emojis) else "✅"
                formatted += f"{emoji} {goal}\n\n"
            formatted += "━━━━━━━━━━━━━━━━━━━━\n"
            formatted += "⏰ 45 min focus → 10 min break!\n"
            formatted += f"💪 Let's crush it today, {user_name}! 🚀"
            await update.message.reply_text(formatted)
        else:
            await update.message.reply_text(
                "🤔 I didn't understand that.\n"
                "Try /start to see all available commands!"
            )
    else:
        await update.message.reply_text(
            "🤔 I didn't understand that.\n"
            "Try /start to see all available commands!"
        )


# ✅ NEW: Handle daily plan input and format it nicely
async def handle_daily_plan(context, chat_id, text):
    goals = text.strip().split("\n")
    formatted = "🗓️ YOUR DAILY PLAN\n"
    formatted += "━━━━━━━━━━━━━━━━━━\n\n"
    for i, goal in enumerate(goals, 1):
        formatted += f"🎯 Task {i}: {goal.strip()}\n"
    formatted += "\n━━━━━━━━━━━━━━━━━━\n"
    formatted += "💡 Tip: Focus on one task at a time!\n"
    formatted += "⏰ Remember to take breaks every 45 mins!\n"
    formatted += "🔥 Let's crush it today, Engineer! 💻"
    await context.bot.send_message(chat_id=chat_id, text=formatted)


     # ✅ Add this new handler function
async def plan_handler(update: Update, context):
    if not context.args:
        await update.message.reply_text(
            "📋 Tell me your goals! Example:\n"
            "/plan Study data structures\nFix login bug\nRead Clean Code"
        )
        return
    
    text = " ".join(context.args)
    goals = text.split(",")  # separate by comma
    
    formatted = "🗓 YOUR DAILY BATTLE PLAN\n"
    formatted += "━━━━━━━━━━━━━━━━━━━━\n\n"
    emojis = ["🥇", "🥈", "🥉", "🎯", "⭐", "💡", "🔥"]
    for i, goal in enumerate(goals):
        emoji = emojis[i] if i < len(emojis) else "✅"
        formatted += f"{emoji} {goal.strip()}\n\n"
    formatted += "━━━━━━━━━━━━━━━━━━━━\n"
    formatted += "⏰ Tip: 45 min focus → 10 min break!\n"
    formatted += "💪 You've got this, Engineer Kaleab! 🚀"
    
    await update.message.reply_text(formatted)

# ✅ NEW: Fallback handler for plain messages like "hi"
async def fallback_handler(update: Update, context):
    text = update.message.text.strip()
    lower = text.lower()
    greetings = ["hi", "hello", "hey", "hiya", "howdy", "sup", "yo"]

    if any(lower == g for g in greetings):
        await update.message.reply_text(
            "👋 Hey! I'm your Engineering Assistant Bot!\n\n"
            "Here's what I can do for you:\n"
            "📝 /summarize — Summarize any text\n"
            "🏗️ /prompt — Generate AI prompts\n"
            "💾 /git — Write git commit messages\n"
            "🔍 /debug — Analyze error logs\n"
            "💡 /tip — Daily engineering tip\n"
            "🧠 /explain — Explain any concept or code\n"
            "📋 /todo — Manage your task list\n"
            "🗓️ /plan — Format your daily goals\n"
            "💾 /save — Save notes to knowledge base\n"
            "❓ /ask — Ask from your knowledge base\n\n"
            "Or use the buttons below! 👇"
        )

    # ✅ Detect daily plan — multi-line or reply to morning reminder
    elif "\n" in text or update.message.reply_to_message:
        goals = [g.strip() for g in text.split("\n") if g.strip()]
        
        if len(goals) >= 2:  # Only format if 2+ lines
            emojis = ["🥇", "🥈", "🥉", "🎯", "⭐", "💡", "🔥", "✅"]
            formatted = "🗓 YOUR DAILY BATTLE PLAN\n"
            formatted += "━━━━━━━━━━━━━━━━━━━━\n\n"
            for i, goal in enumerate(goals):
                emoji = emojis[i] if i < len(emojis) else "✅"
                formatted += f"{emoji} {goal}\n\n"
            formatted += "━━━━━━━━━━━━━━━━━━━━\n"
            formatted += "⏰ 45 min focus → 10 min break!\n"
            formatted += "💪 Let's crush it today! 🚀"
            await update.message.reply_text(formatted)
        else:
            await update.message.reply_text(
                "🤔 I didn't understand that.\n"
                "Try /start to see all available commands!\n\n"
                "💡 Tip: To format your daily plan, type each goal on a new line!"
            )
    else:
        await update.message.reply_text(
            "🤔 I didn't understand that.\n"
            "Try /start to see all available commands!\n\n"
            "💡 Tip: To format your daily plan, type each goal on a new line!"
        )

from telegram import Update

if __name__ == '__main__':
    Thread(target=run).start()
    print("🌍 Keep-alive server started on port 8080...")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    job_queue = application.job_queue

   
    # Register all handlers
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('summarize', summarize_handler))
    application.add_handler(CommandHandler('prompt', prompt_handler))
    application.add_handler(CommandHandler('git', git_handler))
    application.add_handler(CommandHandler('debug', debug_handler))
    application.add_handler(InlineQueryHandler(inline_query_handler))
    application.add_handler(CommandHandler('save', save_handler))
    application.add_handler(CommandHandler('ask', ask_handler))
    application.add_handler(CommandHandler('clear_kb', clear_kb_handler))
    application.add_handler(CommandHandler('plan', plan_handler))
    application.add_handler(CommandHandler('tip', tip_handler))
    application.add_handler(CommandHandler('explain', explain_handler))
    application.add_handler(CommandHandler('todo', todo_handler))
    application.add_handler(MessageHandler(filters.Text("📝 Summarize"), summarize_handler))
    application.add_handler(MessageHandler(filters.Text("🏗️ Prompt Gen"), prompt_handler))
    application.add_handler(MessageHandler(filters.Text("💾 Git Commit"), git_handler))
    application.add_handler(MessageHandler(filters.Text("🔍 Debug Log"), debug_handler))
    application.add_handler(MessageHandler(filters.Text("💡 Daily Tip"), tip_handler))
    application.add_handler(MessageHandler(filters.Text("📋 Todo List"), todo_handler))
    application.add_handler(MessageHandler(filters.Text("🗓️ Plan Your Day"), plan_handler))
    application.add_handler(MessageHandler(filters.PHOTO, image_message_handler))


    # ✅ NEW: Fallback for plain messages (hi, hello, unknown text)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_handler))

    print("🤖 Bot is running with all fixes applied!")
    application.run_polling()