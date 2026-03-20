from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import generate_prompt

async def prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if there is text after the /prompt command
    if not context.args:
        await update.message.reply_text(
            "💡 **How to use:**\n"
            "Type `/prompt [your messy idea]`\n\n"
            "Example: `/prompt create a fastapi login route with jwt`"
        )
        return

    raw_input = " ".join(context.args)
    status_msg = await update.message.reply_text("🏗️ **Architecting your prompt...**")

    refined_prompt = await generate_prompt(raw_input)
    
    # We send it in a code block so it's easy to copy-paste
    await status_msg.edit_text(
        f"✅ **Refined Prompt:**\n\n```\n{refined_prompt}\n```\n\n"
        "Copy this and paste it into ChatGPT or Claude.",
        parse_mode="Markdown"
    )