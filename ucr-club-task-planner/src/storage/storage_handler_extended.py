"""Extra storage operations for task records."""

from __future__ import annotations

import os
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_SERVICE_ACCOUNT_PATH = _PROJECT_ROOT / "service_account.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SPREADSHEET_NAME = os.environ.get("SPREADSHEET_NAME", "ucr-club-task-planner")


def _open_sheet() -> gspread.Worksheet:
    creds = Credentials.from_service_account_file(str(_SERVICE_ACCOUNT_PATH), scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).sheet1


def _normalize_record(record: dict) -> dict:
    return {str(key).strip().lower(): value for key, value in record.items()}


def _normalize_title(title: str) -> str:
    return " ".join(str(title).strip().lower().split())


def _titles_match(saved_title: str, requested_title: str) -> bool:
    saved = _normalize_title(saved_title)
    requested = _normalize_title(requested_title)
    return saved == requested or requested in saved or saved in requested


def get_tasks() -> list[dict]:
    """Return all task rows as dictionaries."""
    try:
        sheet = _open_sheet()
        return [_normalize_record(record) for record in sheet.get_all_records()]
    except Exception:
        return []


def complete_task(task_title: str) -> str:
    """Mark the first task with a matching title as complete."""
    try:
        title = _normalize_title(task_title)

        if not title:
            return "error"

        sheet = _open_sheet()
        records = get_tasks()

        for index, task in enumerate(records, start=2):
            current_title = str(task.get("title", ""))

            if _titles_match(current_title, title):
                sheet.update_cell(index, 3, "complete")
                return "success"

        return "not_found"

    except Exception:
        return "error"


def delete_task(task_title: str) -> str:
    """Delete the first task with a matching title."""
    try:
        title = _normalize_title(task_title)

        if not title:
            return "error"

        sheet = _open_sheet()
        records = get_tasks()

        for index, task in enumerate(records, start=2):
            current_title = str(task.get("title", ""))

            if _titles_match(current_title, title):
                sheet.delete_rows(index)
                return "success"

        return "not_found"

    except Exception:
        return "error"
