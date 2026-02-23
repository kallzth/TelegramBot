from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_ai_response

async def commit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a Git commit message from a diff."""
    if not context.args:
        await update.message.reply_text("Please provide a git diff after the /commit command.")
        return

    diff = " ".join(context.args)
    prompt = f"Please generate a concise and informative Git commit message for the following diff:\n\n```diff\n{diff}\n```"
    ai_response = await get_ai_response(prompt)
    await update.message.reply_text(ai_response)
