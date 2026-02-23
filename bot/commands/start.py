from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Welcome to your personal AI assistant!\n\n"
        "Here are the available commands:\n"
        "/ask <question> - Ask a question to the AI.\n"
        "/summarize <text> - Summarize a block of text.\n"
        "/debug <code_snippet> - Get help debugging code.\n"
        "/commit <diff> - Generate a Git commit message.\n"
        "/help - Show this help message."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a help message when the /help command is issued."""
    await start(update, context)
