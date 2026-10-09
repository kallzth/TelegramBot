from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import quick_explain

async def explain_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if replying to a message with code
    if update.message.reply_to_message:
        concept = update.message.reply_to_message.text
    elif context.args:
        concept = " ".join(context.args)
    else:
        await update.message.reply_text(
            "🧠 CONCEPT EXPLAINER\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Explains any code, concept, or technology\n"
    "in simple terms with a practical example.\n\n"
    "USAGE\n"
    "/explain [concept or code snippet]\n\n"
    "EXAMPLES\n"
    "› /explain what is Big O notation\n"
    "› /explain how does JWT authentication work\n"
    "› /explain the difference between TCP and UDP\n"
    "› /explain [paste a confusing code block]\n\n"
    "OUTPUT\n"
    "Clear 3-4 sentence explanation + practical example."
        )
        return

    status = await update.message.reply_text("🧠 Thinking...")
    try:
        result = await quick_explain(concept)
        await status.edit_text(
            f"🧠 Explanation:\n\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"{result}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"❓ Have more questions? Just ask!"
        )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")