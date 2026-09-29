import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.sheets_utils import log_entry, get_recent_logs

async def log_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📊 Usage: /log [category] [content]\n\n"
            "Examples:\n"
            "/log study Studied Binary Trees for 2 hours\n"
            "/log bug Fixed null pointer in auth module\n"
            "/log idea Build a CLI tool for git automation\n\n"
            "Categories: study, bug, idea, task, note, exam, project"
        )
        return

    args = context.args
    # First word is category if it's a known one
    known_categories = ["study", "bug", "idea", "task", "note", "exam", "project"]
    if args[0].lower() in known_categories:
        category = args[0].capitalize()
        content = " ".join(args[1:])
    else:
        category = "Note"
        content = " ".join(args)

    if not content:
        await update.message.reply_text("❌ Please add some content after the category!")
        return

    status = await update.message.reply_text("📊 Logging to Google Sheets...")

    try:
        user = update.message.from_user.first_name
        await asyncio.to_thread(log_entry, category, content, user)
        await status.edit_text(
            f"✅ Logged successfully!\n\n"
            f"📁 Category: {category}\n"
            f"📝 Content: {content}\n\n"
            f"View your logs: /logview"
        )
    except Exception as e:
        await status.edit_text(f"❌ Error logging: {str(e)}")


async def logview_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = await update.message.reply_text("📊 Fetching your recent logs...")

    try:
        logs = await asyncio.to_thread(get_recent_logs, 5)

        if not logs:
            await status.edit_text(
                "📊 No logs yet!\n"
                "Use /log to start tracking your work."
            )
            return

        response = "📊 YOUR RECENT LOGS\n"
        response += "━━━━━━━━━━━━━━━━━━━━\n\n"

        category_emojis = {
            "Study": "📚",
            "Bug": "🐛",
            "Idea": "💡",
            "Task": "✅",
            "Note": "📝",
            "Exam": "🎓",
            "Project": "🏗️",
        }

        for row in reversed(logs):
            if len(row) >= 4:
                timestamp, user, category, content = row[0], row[1], row[2], row[3]
                emoji = category_emojis.get(category, "📌")
                response += f"{emoji} {category}\n"
                response += f"📅 {timestamp}\n"
                response += f"💬 {content}\n\n"

        response += "━━━━━━━━━━━━━━━━━━━━"
        await status.edit_text(response)

    except Exception as e:
        await status.edit_text(f"❌ Error fetching logs: {str(e)}")