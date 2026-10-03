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
            "/log bug Fixed null pointer in auth module\n\n"
            "💡 To log MULTIPLE items at once, separate with | :\n"
            "/log task Study OS | task Fix login bug | note Buy groceries"
        )
        return

    args_text = " ".join(context.args)
    known_categories = ["study", "bug", "idea", "task", "note", "exam", "project"]
    user = update.message.from_user.first_name

    # ✅ Check for multiple entries separated by |
    if "|" in args_text:
        entries = [e.strip() for e in args_text.split("|") if e.strip()]
        status = await update.message.reply_text(f"📊 Logging {len(entries)} entries...")
        
        success = 0
        results = ""
        for entry in entries:
            parts = entry.split(" ", 1)
            if len(parts) >= 2 and parts[0].lower() in known_categories:
                category = parts[0].capitalize()
                content = parts[1]
            else:
                category = "Note"
                content = entry
            
            try:
                await asyncio.to_thread(log_entry, category, content, user)
                results += f"✅ {category}: {content}\n"
                success += 1
            except Exception as e:
                results += f"❌ Failed: {content}\n"

        await status.edit_text(
            f"📊 Logged {success}/{len(entries)} entries:\n\n"
            f"{results}\n"
            f"View: /logview"
        )
        return

    # Single entry
    parts = args_text.split(" ", 1)
    if parts[0].lower() in known_categories:
        category = parts[0].capitalize()
        content = parts[1] if len(parts) > 1 else ""
    else:
        category = "Note"
        content = args_text

    if not content:
        await update.message.reply_text("❌ Please add content after the category!")
        return

    status = await update.message.reply_text("📊 Logging to Google Sheets...")

    try:
        await asyncio.to_thread(log_entry, category, content, user)
        await status.edit_text(
            f"✅ Logged!\n"
            f"📁 {category}: {content}"
        )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")