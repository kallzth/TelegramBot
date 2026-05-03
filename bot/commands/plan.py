from telegram import Update
from telegram.ext import ContextTypes

async def plan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📋 Usage: /plan Study, Fix bug, Read book\n"
            "(separate tasks with commas)"
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