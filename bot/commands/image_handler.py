import os
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import analyze_image

async def image_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    
    status_msg = await update.message.reply_text("👁️ Analyzing image, please wait...")
    
    file_name = f"img_{update.message.message_id}.jpg"
    await photo_file.download_to_drive(file_name)
    
    try:
        user_prompt = update.message.caption
        analysis = await analyze_image(file_name, user_prompt)
        await status_msg.edit_text(f"🔍 Analysis:\n\n{analysis}")
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error analyzing image: {str(e)}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)