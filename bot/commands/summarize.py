from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_summary

async def summarize_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if this is a reply to a message or has its own text
    text_to_summarize = ""
    
    if update.message.reply_to_message:
        text_to_summarize = update.message.reply_to_message.text
    elif context.args:
        text_to_summarize = " ".join(context.args)
    else:
        await update.message.reply_text("❌ Please reply to a message or provide text after /summarize")
        return

    status_message = await update.message.reply_text("⌛ Processing summary...")
    
    try:
        summary = await get_summary(text_to_summarize)
        await status_message.edit_text(f"📝 **Summary:**\n\n{summary}", parse_mode="Markdown")
    except Exception as e:
        await status_message.edit_text(f"❌ Error: {str(e)}")