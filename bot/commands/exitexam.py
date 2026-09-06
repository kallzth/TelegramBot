from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import ContextTypes, CallbackQueryHandler
from bot.utils.ai_utils import generate_exit_exam_question
import re

COURSE_SHORTCUTS = {
    "🖥️ Programming": "programming",
    "🌳 DSA": "dsa",
    "🧱 OOP": "oop",
    "🌐 Web": "web",
    "📱 Mobile": "mobile",
    "🗄️ Database": "database",
    "⚙️ OS": "os",
    "🛠️ Software Eng": "se",
    "📋 Project Mgmt": "spm",
    "🔌 Networking": "networking",
    "🔐 Security": "security",
    "🤖 AI": "ai",
    "📊 ML": "ml",
    "🎲 Random": "random",
}

def parse_question(raw: str):
    """Parse the AI response into structured parts."""
    try:
        course = re.search(r"COURSE:\s*(.+)", raw).group(1).strip()
        topic = re.search(r"TOPIC:\s*(.+)", raw).group(1).strip()
        question = re.search(r"QUESTION:\n(.+?)(?=\na\))", raw, re.DOTALL).group(1).strip()
        a = re.search(r"a\)\s*(.+)", raw).group(1).strip()
        b = re.search(r"b\)\s*(.+)", raw).group(1).strip()
        c = re.search(r"c\)\s*(.+)", raw).group(1).strip()
        d = re.search(r"d\)\s*(.+)", raw).group(1).strip()
        answer = re.search(r"ANSWER:\s*(.+)", raw).group(1).strip().lower()
        explanation = re.search(r"EXPLANATION:\n(.+)", raw, re.DOTALL).group(1).strip()
        return {
            "course": course, "topic": topic,
            "question": question,
            "options": [a, b, c, d],
            "answer": answer,
            "explanation": explanation
        }
    except Exception:
        return None

async def send_exam_question(update_or_query, context, course="random", is_callback=False):
    """Generate and send a question as a Telegram Poll."""
    raw = await generate_exit_exam_question(course)
    parsed = parse_question(raw)

    if not parsed:
        text = f"🎯 Exit Exam Question:\n\n```\n{raw}\n```"
        if is_callback:
            await update_or_query.edit_message_text(text, parse_mode="Markdown")
        else:
            await update_or_query.message.reply_text(text, parse_mode="Markdown")
        return

    answer_map = {"a": 0, "b": 1, "c": 2, "d": 3}
    correct_index = answer_map.get(parsed["answer"][0], 0)

    # Inline buttons for next question
    keyboard = [
        [
            InlineKeyboardButton("🎲 Random", callback_data="exitexam_random"),
            InlineKeyboardButton("📖 Explain", callback_data=f"explain_{course}"),
        ],
        [
            InlineKeyboardButton("🖥️ Prog", callback_data="exitexam_programming"),
            InlineKeyboardButton("🌳 DSA", callback_data="exitexam_dsa"),
            InlineKeyboardButton("🧱 OOP", callback_data="exitexam_oop"),
        ],
        [
            InlineKeyboardButton("🗄️ DB", callback_data="exitexam_database"),
            InlineKeyboardButton("⚙️ OS", callback_data="exitexam_os"),
            InlineKeyboardButton("🌐 Web", callback_data="exitexam_web"),
        ],
        [
            InlineKeyboardButton("🤖 AI", callback_data="exitexam_ai"),
            InlineKeyboardButton("📊 ML", callback_data="exitexam_ml"),
            InlineKeyboardButton("🔐 Sec", callback_data="exitexam_security"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Store explanation in context for later
    context.user_data["last_explanation"] = (
        f"📚 Course: {parsed['course']}\n"
        f"📌 Topic: {parsed['topic']}\n\n"
        f"✅ Answer: {parsed['answer'].upper()}\n\n"
        f"💡 Explanation:\n{parsed['explanation']}"
    )

        # Send as native Telegram poll
    chat_id = (
        update_or_query.message.chat_id
        if not is_callback
        else update_or_query.message.chat_id
    )

    # Telegram poll question max is 300 chars — truncate if needed
    poll_question = f"📚 {parsed['course']} | {parsed['topic']}\n\n{parsed['question']}"
    if len(poll_question) > 300:
        header = f"📚 {parsed['course']} | {parsed['topic']}\n\n"
        max_q_len = 300 - len(header) - 3
        poll_question = f"{header}{parsed['question'][:max_q_len]}..."

    await context.bot.send_poll(
        chat_id=chat_id,
        question=poll_question,
        options=parsed["options"],
        type="quiz",
        correct_option_id=correct_index,
        explanation=parsed["explanation"][:200],
        is_anonymous=False,
        reply_markup=reply_markup
    )

async def exitexam_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    course = "random"
    if context.args:
        course = context.args[0].lower()

    status = await update.message.reply_text("📝 Generating exit exam question...")
    try:
        await send_exam_question(update, context, course)
        await status.delete()
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")

async def exitexam_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("explain_"):
        explanation = context.user_data.get("last_explanation", "No explanation available.")
        await query.message.reply_text(f"💡 Full Explanation:\n\n{explanation}")
        return

    course = data.replace("exitexam_", "")
    await query.message.reply_text("📝 Generating next question...")
    try:
        await send_exam_question(query, context, course, is_callback=True)
    except Exception as e:
        await query.message.reply_text(f"❌ Error: {str(e)}")