from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import suggest_commit, analyze_error

async def git_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "💾 Usage: /git [what you did]\n\n"
            "Example: /git I added login logic and fixed the navbar"
        )
        return

    raw_input = " ".join(context.args)
    status = await update.message.reply_text("⏳ Generating commit message...")

    try:
        suggestion = await suggest_commit(raw_input)
        response = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💾 GIT COMMIT GENERATOR\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{suggestion}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📋 Copy the COPY-READY section above!"
        )

        # ✅ No parse_mode — avoids Markdown crash
        await status.edit_text(response)
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")

async def debug_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_text = ""
    if update.message.reply_to_message:
        log_text = update.message.reply_to_message.text
    elif context.args:
        log_text = " ".join(context.args)
    else:
        await update.message.reply_text("❌ Paste an error log after /debug or reply to a log message.")
        return

    status = await update.message.reply_text("🔍 Analyzing stack trace...")

    try:
        analysis = await analyze_error(log_text)
        # ✅ No parse_mode — avoids Markdown crash
        await status.edit_text(f"🛠 Debug Report:\n\n{analysis}")
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")