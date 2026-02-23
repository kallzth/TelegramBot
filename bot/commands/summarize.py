from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_ai_response

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Summarizes a block of text."""
    if not context.args:
        await update.message.reply_text("Please provide text to summarize after the /summarize command.")
        return

    text_to_summarize = " ".join(context.args)
    prompt = f"Please summarize the following text:\n\n{text_to_summarize}"
    ai_response = await get_ai_response(prompt)
    await update.message.reply_text(ai_response)
