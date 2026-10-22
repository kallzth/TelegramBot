from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.user_tracker import save_user

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    save_user(user.id, user.first_name, user.username)
    
    keyboard = [
        
            ['📝 Summarize', '🏗️ Prompt Gen'],
            ['💾 Git Commit', '🔍 Debug Log'],
            ['💡 Daily Tip', '📋 Todo List'],
            ['📄 README Gen', '🎤 Interview'],
            ['🎓 Exit Exam', '🗓️ Plan Your Day'],
            ['📊 Log', '📚 Tutor'],

    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"👋 Hey {user_name}! Welcome to Engineer HQ Bot!\n\n"
        f"I'm your personal software engineering assistant.\n"
        f"Select a tool from the menu below:",
        reply_markup=reply_markup,
    )