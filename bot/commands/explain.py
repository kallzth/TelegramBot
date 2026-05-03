from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import quick_explain

async def explain_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if replying to a message with code
    if update.message.reply_to_message:
        concept = update.message.reply_to_message.text
    elif context.args:
        concept = " ".join(context.args)
    else:
        await update.message.reply_text(
            "💡 Usage: /explain [concept or code]\n\n"
            "Examples:\n"
            "• /explain what is a binary tree\n"
            "• /explain async await in Python\n"
            "• Reply to any code message with /explain"
        )
        return

    status = await update.message.reply_text("🧠 Thinking...")
    try:
        result = await quick_explain(concept)
        await status.edit_text(
            f"🧠 Explanation:\n\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"{result}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"❓ Have more questions? Just ask!"
        )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")