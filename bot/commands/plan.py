from telegram import Update
from telegram.ext import ContextTypes

async def plan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🗓️ DAILY PLANNER\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Formats your daily goals into a structured\n"
            "battle plan with priority ordering.\n\n"
            "USAGE\n"
            "/plan [goal 1], [goal 2], [goal 3]\n\n"
            "EXAMPLES\n"
            "› /plan Study data structures, Fix login bug, Read Clean Code\n"
            "› /plan Review PR, Write unit tests, Update documentation\n\n"
            "— OR — send goals on separate lines:\n\n"
            "Study data structures\n"
            "Fix login bug\n"
            "Read Clean Code\n\n"
            "OUTPUT\n"
            "Prioritized battle plan with focus time reminders."
        )
        return

    text = " ".join(context.args)
    goals = text.split(",")

    formatted = "🗓 YOUR DAILY BATTLE PLAN\n"
    formatted += "━━━━━━━━━━━━━━━━━━━━\n\n"
    emojis = ["🥇", "🥈", "🥉", "🎯", "⭐", "💡", "🔥"]
    for i, goal in enumerate(goals):
        emoji = emojis[i] if i < len(emojis) else "✅"
        formatted += f"{emoji} {goal.strip()}\n\n"
    formatted += "━━━━━━━━━━━━━━━━━━━━\n"
    formatted += "⏰ 45 min focus → 10 min break!\n"
    formatted += "💪 Let's crush it, Engineer Kaleab! 🚀"

    await update.message.reply_text(formatted)