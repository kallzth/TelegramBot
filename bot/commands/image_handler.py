import os
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import analyze_image

async def image_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the highest resolution version of the photo
    photo_file = await update.message.photo[-1].get_file()
    
    status_msg = await update.message.reply_text("👁️ **Scanning image...**", parse_mode="Markdown")
    
    # 1. Download locally
    file_name = f"img_{update.message.message_id}.jpg"
    await photo_file.download_to_drive(file_name)
    
    try:
        # Check if the user sent a caption (e.g., "What is wrong here?")
        user_prompt = update.message.caption
        
        # 2. AI Analysis
        analysis = await analyze_image(file_name, user_prompt)
        
        # 3. Reply
        await status_msg.edit_text(f"🔍 **AI Vision Analysis:**\n\n{analysis}", parse_mode="Markdown")
        
    finally:
        # 4. Cleanup
        if os.path.exists(file_name):
            os.remove(file_name)