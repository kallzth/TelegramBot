import json
import os
from telegram import Update
from telegram.ext import ContextTypes

TODO_FILE = "bot/todos.json"

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f)

async def todo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    todos = load_todos()

    if not context.args:
        # Show current todo list
        if not todos:
            await update.message.reply_text(
                "📋 Your todo list is empty!\n\n"
                "Add tasks with: /todo add Buy groceries\n"
                "Done a task with: /todo done 1\n"
                "Clear all with: /todo clear"
            )
            return

        msg = "📋 YOUR TODO LIST\n━━━━━━━━━━━━━━━━━━\n\n"
        for i, item in enumerate(todos, 1):
            status = "✅" if item["done"] else "⬜"
            msg += f"{status} {i}. {item['task']}\n"
        
        pending = sum(1 for t in todos if not t["done"])
        done = sum(1 for t in todos if t["done"])
        msg += f"\n━━━━━━━━━━━━━━━━━━\n"
        msg += f"⬜ Pending: {pending}  ✅ Done: {done}"
        await update.message.reply_text(msg)
        return

    action = context.args[0].lower()

    if action == "add":
        if len(context.args) < 2:
            await update.message.reply_text("❌ Usage: /todo add [task name]")
            return
        task = " ".join(context.args[1:])
        todos.append({"task": task, "done": False})
        save_todos(todos)
        await update.message.reply_text(
            f"✅ Added to your list:\n⬜ {task}\n\n"
            f"You now have {len(todos)} task(s). Let's get it done! 💪"
        )

    elif action == "done":
        if len(context.args) < 2 or not context.args[1].isdigit():
            await update.message.reply_text("❌ Usage: /todo done [task number]")
            return
        idx = int(context.args[1]) - 1
        if idx < 0 or idx >= len(todos):
            await update.message.reply_text("❌ Invalid task number!")
            return
        todos[idx]["done"] = True
        save_todos(todos)
        await update.message.reply_text(
            f"🎉 Marked as done:\n✅ {todos[idx]['task']}\n\n"
            f"Great work, Engineer Kaleab! 🔥"
        )

    elif action == "remove":
        if len(context.args) < 2 or not context.args[1].isdigit():
            await update.message.reply_text("❌ Usage: /todo remove [task number]")
            return
        idx = int(context.args[1]) - 1
        if idx < 0 or idx >= len(todos):
            await update.message.reply_text("❌ Invalid task number!")
            return
        removed = todos.pop(idx)
        save_todos(todos)
        await update.message.reply_text(f"🗑 Removed: {removed['task']}")

    elif action == "clear":
        save_todos([])
        await update.message.reply_text("🧹 Todo list cleared! Fresh start! 🚀")

    else:
        await update.message.reply_text(
            "❌ Unknown action. Use:\n"
            "/todo — View list\n"
            "/todo add [task] — Add task\n"
            "/todo done [number] — Mark done\n"
            "/todo remove [number] — Remove task\n"
            "/todo clear — Clear all"
        )