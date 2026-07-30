from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from bot.utils.ai_utils import generate_interview_question

async def interview_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Determine category from args
    category = "random"
    if context.args:
        arg = context.args[0].lower()
        if arg in ["technical", "tech"]:
            category = "technical"
        elif arg in ["behavioral", "behaviour", "hr"]:
            category = "behavioral"

    status = await update.message.reply_text("🎯 Preparing your interview question...")

    try:
        question = await generate_interview_question(category)

        # Inline buttons for next question
        keyboard = [
            [
                InlineKeyboardButton("🔁 New Question", callback_data="interview_random"),
                InlineKeyboardButton("💻 Technical", callback_data="interview_technical"),
            ],
            [
                InlineKeyboardButton("🤝 Behavioral", callback_data="interview_behavioral"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await status.edit_text(
            f"🎯 *Mock Interview Question:*\n\n```\n{question}\n```\n\n"
            "Type your answer and reflect on it! 💪",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")


async def interview_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("interview_", "")
    await query.edit_message_text("🎯 Preparing your next question...")

    try:
        question = await generate_interview_question(category)

        keyboard = [
            [
                InlineKeyboardButton("🔁 New Question", callback_data="interview_random"),
                InlineKeyboardButton("💻 Technical", callback_data="interview_technical"),
            ],
            [
                InlineKeyboardButton("🤝 Behavioral", callback_data="interview_behavioral"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🎯 *Mock Interview Question:*\n\n```\n{question}\n```\n\n"
            "Type your answer and reflect on it! 💪",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)}")