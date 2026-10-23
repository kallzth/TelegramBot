import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.core.config import DEVELOPER_ID
from bot.utils.user_tracker import get_all_users, get_user_count

async def announce_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send an announcement to all bot users. Developer only."""
    user_id = update.message.from_user.id

    # ✅ Check if sender is the developer
    if user_id != DEVELOPER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if not context.args:
        count = get_user_count()
        await update.message.reply_text(
            "ANNOUNCEMENT SYSTEM\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"Total users: {count}\n\n"
            "USAGE\n"
            "/announce [your message]\n\n"
            "EXAMPLES\n"
            "> /announce New feature added: /review command is now live!\n"
            "> /announce Bot will be down for maintenance at 2AM UTC\n\n"
            "The message will be sent to ALL bot users."
        )
        return

    message = " ".join(context.args)
    users = get_all_users()

    if not users:
        await update.message.reply_text("❌ No users found. Users are tracked when they use /start.")
        return

    announcement = (
        "📢 ANNOUNCEMENT FROM KALDEV BOT\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{message}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "KalDev Bot — @Kalhelp_Bot"
    )

    status = await update.message.reply_text(
        f"📢 Sending announcement to {len(users)} users..."
    )

    success = 0
    failed = 0

    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user["user_id"],
                text=announcement
            )
            success += 1
            # Small delay to avoid Telegram rate limits
            await asyncio.sleep(0.05)
        except Exception as e:
            failed += 1
            print(f"Failed to send to {user['user_id']}: {e}")

    await status.edit_text(
        f"📢 Announcement sent!\n\n"
        f"✅ Delivered: {success}\n"
        f"❌ Failed: {failed}\n"
        f"Total: {len(users)}"
    )


async def users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user stats. Developer only."""
    user_id = update.message.from_user.id

    if user_id != DEVELOPER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    users = get_all_users()

    if not users:
        await update.message.reply_text("No users tracked yet.")
        return

    response = f"USER STATS\n"
    response += "━━━━━━━━━━━━━━━━━━━━\n\n"
    response += f"Total users: {len(users)}\n\n"
    response += "RECENT USERS\n"

    for user in users[-10:]:
        username = f"@{user['username']}" if user.get('username') else "no username"
        response += f"› {user['first_name']} ({username}) — ID: {user['user_id']}\n"

    await update.message.reply_text(response)