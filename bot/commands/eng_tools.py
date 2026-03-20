from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import suggest_commit, analyze_error

async def git_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/git I added login logic and fixed the navbar`", parse_mode="Markdown")
        return
    
    raw_input = " ".join(context.args)
    suggestion = await suggest_commit(raw_input)
    await update.message.reply_text(f"📝 **Suggested Commit:**\n\n`{suggestion}`", parse_mode="Markdown")

async def debug_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle both direct text and replies to long logs
    log_text = ""
    if update.message.reply_to_message:
        log_text = update.message.reply_to_message.text
    elif context.args:
        log_text = " ".join(context.args)
    else:
        await update.message.reply_text("❌ Paste an error log after /debug or reply to a log message.")
        return

    status = await update.message.reply_text("🔍 **Analyzing stack trace...**", parse_mode="Markdown")
    analysis = await analyze_error(log_text)
    await status.edit_text(f"🛠 **Debug Report:**\n\n{analysis}", parse_mode="Markdown")