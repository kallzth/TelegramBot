from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import save_to_kb, search_kb, clear_kb_file

async def save_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # If the user replies to a message with /save, save that message
    if update.message.reply_to_message:
        text_to_save = update.message.reply_to_message.text
    elif context.args:
        text_to_save = " ".join(context.args)
    else:
        await update.message.reply_text("❌ Reply to a message with /save or type text after it.")
        return

    save_to_kb(text_to_save)
    await update.message.reply_text(f"✅ Saved to memory: \"{text_to_save[:20]}...\"")

async def ask_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/ask How did I fix that Prisma error?`")
        return
    
    query = " ".join(context.args)
    status = await update.message.reply_text("🧠 **Searching your memory...**", parse_mode="Markdown")
    answer = await search_kb(query)
    await status.edit_text(f"📖 **Knowledge Base Result:**\n\n{answer}", parse_mode="Markdown")

async def clear_kb_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    success = clear_kb_file()
    if success:
        await update.message.reply_text("🗑️ **Memory Wiped.** Your Knowledge Base is now empty.", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ **Error:** Could not clear the memory file.")