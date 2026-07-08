from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import generate_readme

async def readme_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args and (not update.message.text or update.message.text.strip() == "📄 README Gen"):
        await update.message.reply_text(
            "📄 Usage: /readme [describe your project]\n\n"
            "Example:\n"
            "/readme A Telegram bot built with Python and Gemini AI that helps software engineers with daily tasks"
        )
        return

    description = " ".join(context.args) if context.args else update.message.text
    status = await update.message.reply_text("📝 Generating your README...")

    try:
        readme = await generate_readme(description)

        MAX_LENGTH = 3900
        if len(readme) <= MAX_LENGTH:
            await status.edit_text(
                f"📄 *Your README.md:*\n\n```\n{readme}\n```\n\n"
                "Copy and paste this into your `README.md` file!",
                parse_mode="Markdown"
            )
        else:
            await status.delete()
            chunks = [readme[i:i+MAX_LENGTH] for i in range(0, len(readme), MAX_LENGTH)]
            for i, chunk in enumerate(chunks):
                prefix = f"📄 *Your README.md (Part {i+1}/{len(chunks)}):*\n\n" if i == 0 else f"*(Part {i+1}/{len(chunks)})*\n\n"
                await update.message.reply_text(
                    f"{prefix}```\n{chunk}\n```",
                    parse_mode="Markdown"
                )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")