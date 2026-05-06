import json
import os
from telegram import Update
from telegram.ext import ContextTypes

TODO_FILE = "bot/todos.json"

def load_all_todos():
    if not os.path.exists(TODO_FILE):
        return {}
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_all_todos(all_todos):
    with open(TODO_FILE, "w") as f:
        json.dump(all_todos, f)

def get_user_todos(user_id: str):
    all_todos = load_all_todos()
    return all_todos.get(user_id, [])

def save_user_todos(user_id: str, todos: list):
    all_todos = load_all_todos()
    all_todos[user_id] = todos
    save_all_todos(all_todos)

async def todo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.first_name
    todos = get_user_todos(user_id)

    if not context.args:
        if not todos:
            await update.message.reply_text(
                f"📋 Hey {user_name}, your todo list is empty!\n\n"
                "Add tasks with: /todo add Buy groceries\n"
                "Mark done with: /todo done 1\n"
                "Remove with: /todo remove 1\n"
                "Clear all with: /todo clear"
            )
            return

        msg = f"📋 {user_name.upper()}'S TODO LIST\n━━━━━━━━━━━━━━━━━━\n\n"
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
        save_user_todos(user_id, todos)
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
        save_user_todos(user_id, todos)
        await update.message.reply_text(
            f"🎉 Marked as done:\n✅ {todos[idx]['task']}\n\nGreat work, {user_name}! 🔥"
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
        save_user_todos(user_id, todos)
        await update.message.reply_text(f"🗑 Removed: {removed['task']}")

    elif action == "clear":
        save_user_todos(user_id, [])
        await update.message.reply_text(f"🧹 Todo list cleared, {user_name}! Fresh start! 🚀")

    else:
        await update.message.reply_text(
            "❌ Unknown action. Use:\n"
            "/todo — View list\n"
            "/todo add [task] — Add task\n"
            "/todo done [number] — Mark done\n"
            "/todo remove [number] — Remove task\n"
            "/todo clear — Clear all"
        )