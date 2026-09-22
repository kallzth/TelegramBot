import gspread
import os
import json
import asyncio
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime
import pytz

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
ADDIS_TZ = pytz.timezone("Africa/Addis_Ababa")

def get_credentials():
    """Load credentials from environment variable or local token.json."""
    token_json = os.getenv("GOOGLE_TOKEN_JSON")
    
    if token_json:
        token_data = json.loads(token_json)
    else:
        with open("token.json", "r") as f:
            token_data = json.load(f)

    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes")
    )

    # Auto-refresh if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds

def get_sheet(sheet_name: str):
    """Connect to Google Sheets and return the worksheet."""
    creds = get_credentials()
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)
    try:
        return spreadsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(
            title=sheet_name, rows=1000, cols=10
        )
        return sheet

def log_entry(category: str, content: str, user: str = "Kaleab"):
    """Log an entry to the Logs sheet."""
    sheet = get_sheet("Logs")

    if not sheet.get_all_values():
        sheet.append_row(["Timestamp", "User", "Category", "Content"])

    now = datetime.now(ADDIS_TZ).strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, user, category, content])

def get_recent_logs(limit: int = 5) -> list:
    """Get the most recent log entries."""
    sheet = get_sheet("Logs")
    all_rows = sheet.get_all_values()

    if len(all_rows) <= 1:
        return []

    data_rows = all_rows[1:]
    return data_rows[-limit:]

def log_exam_score(course: str, topic: str, is_correct: bool, user: str = "Kaleab"):
    """Log exit exam quiz results."""
    sheet = get_sheet("Exam Scores")

    if not sheet.get_all_values():
        sheet.append_row(["Timestamp", "User", "Course", "Topic", "Result"])

    now = datetime.now(ADDIS_TZ).strftime("%Y-%m-%d %H:%M:%S")
    result = "✅ Correct" if is_correct else "❌ Wrong"
    sheet.append_row([now, user, course, topic, result])