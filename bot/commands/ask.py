from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_ai_response

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Asks a question to the AI model."""
    if not context.args:
        await update.message.reply_text("Please provide a question after the /ask command.")
        return

    question = " ".join(context.args)
    prompt = f"Question: {question}\nAnswer:"
    ai_response = await get_ai_response(prompt)
    await update.message.reply_text(ai_response)
