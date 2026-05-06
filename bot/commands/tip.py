from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import get_daily_tip

async def tip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    status = await update.message.reply_text("💡 Fetching your engineering tip...")
    try:
        tip = await get_daily_tip()
        await status.edit_text(
            f"💡 Daily Engineering Tip:\n\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"{tip}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔥 Keep learning, Engineer {user_name}!"
        )
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")