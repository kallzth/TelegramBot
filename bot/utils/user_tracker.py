import json
import os

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "users.json")

def load_users() -> dict:
    """Load all tracked users from file."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_user(user_id: int, first_name: str, username: str = None):
    """Save a user to the tracking file."""
    users = load_users()
    users[str(user_id)] = {
        "first_name": first_name,
        "username": username or "",
        "user_id": user_id
    }
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print(f"DEBUG: Failed to save user: {e}")

def get_all_users() -> list:
    """Get all tracked users as a list."""
    users = load_users()
    return list(users.values())

def get_user_count() -> int:
    """Get total number of tracked users."""
    return len(load_users())