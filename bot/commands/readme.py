from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import generate_readme

async def readme_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📄 Usage: /readme [describe your project]\n\n"
            "Example:\n"
            "/readme A Telegram bot built with Python and Gemini AI that helps software engineers with daily tasks"
        )
        return

    description = " ".join(context.args)
    status = await update.message.reply_text("📝 Generating your README...")

    try:
        readme = await generate_readme(description)
        await status.edit_text(
            f"📄 *Your README.md:*\n\n```\n{readme}\n```\n\n"
            "Copy and paste this into your `README.md` file!",
            parse_mode="Markdown"
        )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")