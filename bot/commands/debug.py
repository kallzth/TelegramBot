from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_ai_response

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Helps debug a code snippet."""
    if not context.args:
        await update.message.reply_text("Please provide a code snippet to debug after the /debug command.")
        return

    code_snippet = " ".join(context.args)
    prompt = f"Please help me debug the following code:\n\n```\n{code_snippet}\n```"
    ai_response = await get_ai_response(prompt)
    await update.message.reply_text(ai_response)
