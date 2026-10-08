from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_ai_response

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Helps debug a code snippet."""
    if not context.args:
        await update.message.reply_text( 
    "🔍 DEBUG ANALYZER\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Analyzes error logs and stack traces,\n"
    "then provides 3 actionable fix steps.\n\n"
    "USAGE\n"
    "/debug [paste your error log]\n\n"
    "— OR —\n\n"
    "Reply to any error message with /debug\n\n"
    "EXAMPLES\n"
    "› /debug TypeError: cannot read property of undefined\n"
    "› /debug [paste full stack trace]\n\n"
    "OUTPUT\n"
    "Root cause analysis + 3 step-by-step fix suggestions.")
        return

    code_snippet = " ".join(context.args)
    prompt = f"Please help me debug the following code:\n\n```\n{code_snippet}\n```"
    ai_response = await get_ai_response(prompt)
    await update.message.reply_text(ai_response)
