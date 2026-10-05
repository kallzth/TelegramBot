from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import generate_prompt

async def prompt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if there is text after the /prompt command
    if not context.args:

        await update.message.reply_text(
    "🏗️ PROMPT GENERATOR\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "Transforms raw ideas into structured AI prompts\n"
    "using the RTF (Role, Task, Format) framework.\n\n"
    "USAGE\n"
    "/prompt [your idea or task]\n\n"
    "EXAMPLES\n"
    "› /prompt create a fastapi login route with jwt\n"
    "› /prompt write a cover letter for a software engineer\n"
    "› /prompt explain binary search to a 10 year old\n\n"
    "OUTPUT\n"
    "A copy-ready structured prompt for ChatGPT or Claude."
)
        return

    raw_input = " ".join(context.args)+ "\n\nIMPORTANT: Keep your response under 3500 characters."
    status_msg = await update.message.reply_text("🏗️ **Architecting your prompt...**")

    refined_prompt = await generate_prompt(raw_input)
    
    # We send it in a code block so it's easy to copy-paste
    await status_msg.edit_text(
        f"✅ **Refined Prompt:**\n\n```\n{refined_prompt}\n```\n\n"
        "Copy this and paste it into ChatGPT or Claude.",
        parse_mode="Markdown"
    )