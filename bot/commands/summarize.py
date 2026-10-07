from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_summary

async def summarize_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_summarize = ""

    if update.message.reply_to_message:
        text_to_summarize = update.message.reply_to_message.text
    elif context.args:
        text_to_summarize = " ".join(context.args)
    else:
        await update.message.reply_text("📝 SUMMARIZER\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Condenses any text into clear, structured bullet points.\n\n"
    "USAGE\n"
    "/summarize [paste your text here]\n\n"
    "EXAMPLES\n"
    "› /summarize [paste an article]\n"
    "› /summarize [paste lecture notes]\n"
    "› /summarize [paste a research paper]\n\n"
    "OUTPUT\n"
    "Bullet-point summary with key insights highlighted."
    )
        return

    status_message = await update.message.reply_text("⏳ Processing summary...")

    try:
        summary = await get_summary(text_to_summarize)
        # Remove parse_mode to avoid special character crashes
        await status_message.edit_text(f"📝 Summary:\n\n{summary}")
    except Exception as e:
        await status_message.edit_text(f"❌ Error: {str(e)}")