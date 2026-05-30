from __future__ import annotations

import os
from pathlib import Path

import gspread


REQUIRED_KEYS = {"title", "due_date", "status"}
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SERVICE_ACCOUNT_PATH = PROJECT_ROOT / "service_account.json"
SPREADSHEET_NAME = os.environ.get("SPREADSHEET_NAME", "ucr-club-task-planner")


def _get_worksheet():
    from google.oauth2.service_account import Credentials

    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_PATH), scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).sheet1


def save_task(task_data: dict) -> str:
    """Save a task to Google Sheets.

    Returns `success`, `exists`, or `error`.
    """
    try:
        if not REQUIRED_KEYS.issubset(task_data.keys()):
            return "error"

        title = str(task_data["title"]).strip()
        if not title:
            return "error"

        ws = _get_worksheet()

        existing_titles = [value.strip().lower() for value in ws.col_values(1)]
        if title.lower() in existing_titles:
            return "exists"

        ws.append_row([
            title,
            task_data["due_date"],
            task_data["status"],
        ])

        return "success"

    except Exception:
        return "error"
