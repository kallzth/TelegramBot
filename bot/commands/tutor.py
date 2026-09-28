import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.ai_utils import generate_tutor_questions

SUBJECTS = {
    "math": "Mathematics",
    "science": "Science", 
    "english": "English",
    "social": "Social Studies",
    "ict": "ICT"
}

async def send_long_tutor_message(message, text: str):
    """Split long tutor responses."""
    MAX_LENGTH = 4000
    if len(text) <= MAX_LENGTH:
        await message.reply_text(text)
    else:
        chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]
        for i, chunk in enumerate(chunks):
            prefix = f"📚 (Part {i+1}/{len(chunks)})\n\n" if len(chunks) > 1 else ""
            await message.reply_text(prefix + chunk)


async def tutor_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tutor command with text topic."""
    
    # Check if this is a photo with /tutor caption
    if update.message.photo:
        await handle_tutor_image(update, context)
        return

    if not context.args:
        await update.message.reply_text(
            "📚 PEARSON CURRICULUM AI TUTOR\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "I generate 10 practice questions from foundational to challenging!\n\n"
            "📝 TEXT USAGE:\n"
            "/tutor [topic] year=[1-9]\n\n"
            "EXAMPLES:\n"
            "/tutor fractions year=4\n"
            "/tutor photosynthesis year=7\n"
            "/tutor grammar punctuation year=5\n"
            "/tutor algebra equations year=8\n\n"
            "📸 IMAGE USAGE:\n"
            "Send a photo of your textbook/worksheet with caption:\n"
            "/tutor year=6\n\n"
            "SUBJECTS: Mathematics, Science, English,\n"
            "Social Studies, ICT\n"
            "YEARS: 1 to 9"
        )
        return

    # Parse args for year
    args_text = " ".join(context.args)
    year = None
    topic = args_text

    # Extract year= parameter
    if "year=" in args_text.lower():
        parts = args_text.lower().split("year=")
        topic = parts[0].strip()
        year_part = parts[1].strip().split()[0]
        if year_part.isdigit() and 1 <= int(year_part) <= 9:
            year = year_part

    if not topic:
        await update.message.reply_text("❌ Please provide a topic!\nExample: /tutor fractions year=4")
        return

    status = await update.message.reply_text(
        f"📚 Generating 10 practice questions on *{topic}*...\n"
        f"⏳ Please wait...",
        parse_mode="Markdown"
    )

    try:
        questions = await generate_tutor_questions(topic, year)
        await status.delete()
        await send_long_tutor_message(update.message, f"📚 PEARSON CURRICULUM PRACTICE\n\n{questions}")
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")


async def handle_tutor_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image submission for tutor."""
    photo_file = await update.message.photo[-1].get_file()
    
    # Parse year from caption
    caption = update.message.caption or ""
    year = None
    if "year=" in caption.lower():
        parts = caption.lower().split("year=")
        year_part = parts[1].strip().split()[0]
        if year_part.isdigit() and 1 <= int(year_part) <= 9:
            year = year_part

    status = await update.message.reply_text(
        "📚 Analyzing your image and generating 10 practice questions...\n"
        "⏳ Please wait..."
    )

    file_name = f"tutor_{update.message.message_id}.jpg"
    await photo_file.download_to_drive(file_name)

    try:
        topic = f"the content shown in this image"
        questions = await generate_tutor_questions(topic, year, image_path=file_name)
        await status.delete()
        await send_long_tutor_message(update.message, f"📚 PEARSON CURRICULUM PRACTICE\n\n{questions}")
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)


async def tutor_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photos sent with /tutor caption."""
    caption = update.message.caption or ""
    if "/tutor" in caption.lower():
        await handle_tutor_image(update, context)