import os
import re
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.ai_utils import analyze_image

def format_as_html(text: str) -> str:
    """Convert Gemini response to Telegram-safe HTML."""
    
    # Convert \frac{a}{b} → (a/b)
    text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', text)
    # Convert \sqrt{x} → sqrt(x)
    text = re.sub(r'\\sqrt\{([^}]+)\}', r'√(\1)', text)
    # Remove LaTeX delimiters $$ ... $$
    text = re.sub(r'\$\$(.+?)\$\$', r'\1', text, flags=re.DOTALL)
    # Remove inline $ ... $
    text = re.sub(r'\$(.+?)\$', r'\1', text)
    # Replace LaTeX arrows/symbols
    text = text.replace(r'\Rightarrow', '→')
    text = text.replace(r'\rightarrow', '→')
    text = text.replace(r'\cdot', '·')
    text = text.replace(r'\times', '×')
    text = text.replace(r'\div', '÷')
    text = text.replace(r'\partial', '∂')
    text = text.replace(r'\infty', '∞')
    text = text.replace(r'\pi', 'π')
    text = text.replace(r'\alpha', 'α')
    text = text.replace(r'\beta', 'β')
    text = text.replace(r'\theta', 'θ')
    text = text.replace(r'\ln', 'ln')
    text = text.replace(r'\log', 'log')
    text = text.replace(r'\left', '')
    text = text.replace(r'\right', '')
    # Remove remaining backslash commands
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    # Remove leftover braces
    text = re.sub(r'[{}]', '', text)
    # Convert **bold** → <b>bold</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Convert *italic* → <i>italic</i>
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Convert `code` → <code>code</code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Convert ```code blocks``` → <pre>code</pre>
    text = re.sub(r'```(?:\w+)?\n?(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)
    # Escape any remaining HTML special chars outside of tags
    # Clean up extra blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

async def send_long_message(message, text: str):
    """Split and send messages that exceed Telegram's 4096 char limit."""
    MAX_LENGTH = 4000
    if len(text) <= MAX_LENGTH:
        await message.reply_text(text, parse_mode="HTML")
    else:
        chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]
        for i, chunk in enumerate(chunks):
            prefix = f"<b>(Part {i+1}/{len(chunks)})</b>\n\n" if len(chunks) > 1 else ""
            await message.reply_text(prefix + chunk, parse_mode="HTML")

async def image_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    status_msg = await update.message.reply_text("👁️ Analyzing image, please wait...")

    file_name = f"img_{update.message.message_id}.jpg"
    await photo_file.download_to_drive(file_name)

    try:
        user_prompt = update.message.caption
        analysis = await analyze_image(file_name, user_prompt)
        formatted = format_as_html(analysis)

        await status_msg.delete()
        await send_long_message(update.message, f"🔍 <b>Analysis:</b>\n\n{formatted}")

    except Exception as e:
        await status_msg.edit_text(f"❌ Error analyzing image: {str(e)}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)