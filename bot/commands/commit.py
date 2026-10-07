from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_ai_response

async def commit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a Git commit message from a diff."""
    if not context.args:
        await update.message.reply_text(
    "💾 GIT COMMIT GENERATOR\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Converts plain descriptions into professional\n"
    "Conventional Commit messages with a copy button.\n\n"
    "USAGE\n"
    "/git [what you changed]\n\n"
    "EXAMPLES\n"
    "› /git added jwt auth to the login endpoint\n"
    "› /git fixed null pointer in user profile page\n"
    "› /git refactored database connection pooling\n\n"
    "COMMIT TYPES\n"
    "feat · fix · docs · style · refactor · test · chore")
        return

    diff = " ".join(context.args)
    prompt = f"Please generate a concise and informative Git commit message for the following diff:\n\n```diff\n{diff}\n```"
    ai_response = await get_ai_response(prompt)
    await update.message.reply_text(ai_response)
