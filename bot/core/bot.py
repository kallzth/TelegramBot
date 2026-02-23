from telegram.ext import Application, CommandHandler
from bot.core.config import TELEGRAM_BOT_TOKEN
from bot.commands.start import start, help_command
from bot.commands.ask import ask
from bot.commands.summarize import summarize
from bot.commands.debug import debug
from bot.commands.commit import commit

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ask", ask))
    application.add_handler(CommandHandler("summarize", summarize))
    application.add_handler(CommandHandler("debug", debug))
    application.add_handler(CommandHandler("commit", commit))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
