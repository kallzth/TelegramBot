from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # These strings must match your MessageHandlers in main.py exactly
    keyboard = [
        ['📝 Summarize', '🏗️ Prompt Gen'],
        ['💾 Git Commit', '🔍 Debug Log']
        ['💡 Daily Tip', '📋 Todo List'],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🚀 **Engineer HQ Online.**\nSelect a tool from the menu below:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )