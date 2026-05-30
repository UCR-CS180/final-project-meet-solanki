"""Engine layer for the UCR Club Task Planner."""

from __future__ import annotations

import json
import os
import re

from dotenv import load_dotenv
from google import genai

from src.storage.storage_handler import save_task
from src.storage.storage_handler_extended import complete_task, delete_task, get_tasks

load_dotenv()

_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
_MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")

_EXTRACTION_PROMPT = """
You are a task planner engine for a UCR club assistant. Analyze the user request and extract:
- intent: exactly one of "add", "list", "complete", "delete", "unknown"
- data: a dict containing any fields mentioned (title, due_date)

Return strict JSON only:
{"intent": "<intent>", "data": {}}
""".strip()

_REFLECTION_PROMPT = """
You are a data completeness validator.

Extracted data and intent:
{extracted}

Validation rules:
- "add" requires title.
- "complete" requires title.
- "delete" requires title.
- "list" and "unknown" have no required fields.

Return strict JSON only:
{{"complete": <true|false>, "missing": ["<field>", ...]}}
""".strip()


def _model_json(contents: str, system_instruction: str | None = None) -> dict:
    """Ask Gemini for JSON and parse the response."""
    if not _API_KEY:
        raise RuntimeError("Missing API key")

    config = {"response_mime_type": "application/json"}
    if system_instruction is not None:
        config["system_instruction"] = system_instruction

    client = genai.Client(api_key=_API_KEY)
    response = client.models.generate_content(
        model=_MODEL,
        contents=contents,
        config=config,
    )
    return json.loads(response.text)


def _clean_title(title: str) -> str:
    return title.strip(" .,:;")


def _normalize_task_title(title: str) -> str:
    title = _clean_title(title).lower()
    if title.startswith("task "):
        title = title.removeprefix("task ").strip()
    return title


def _fallback_extract(user_input: str) -> dict:
    """Small parser used when Gemini is unavailable during tests."""
    text = user_input.strip()
    lowered = text.lower()
    data: dict[str, str] = {}

    if any(word in lowered for word in ("show", "list")) and "task" in lowered:
        return {"intent": "list", "data": data}

    add_match = re.search(
        r"add (?:a )?task(?: to)? (?P<title>.+?)(?: by (?P<due_date>.+))?$",
        text,
        flags=re.IGNORECASE,
    )
    if add_match:
        title = _clean_title(add_match.group("title"))
        if title:
            data["title"] = title
        if add_match.group("due_date"):
            data["due_date"] = _clean_title(add_match.group("due_date"))
        return {"intent": "add", "data": data}

    if lowered.startswith("add"):
        return {"intent": "add", "data": data}

    complete_match = re.search(
        r"(?:mark )?(?P<title>.+?) complete$",
        text.rstrip("."),
        flags=re.IGNORECASE,
    )
    if complete_match:
        title = _clean_title(complete_match.group("title"))
        if title:
            data["title"] = title
        return {"intent": "complete", "data": data}

    delete_match = re.search(r"delete (?P<title>.+)$", text, flags=re.IGNORECASE)
    if delete_match:
        title = _clean_title(delete_match.group("title"))
        if title:
            data["title"] = title
        return {"intent": "delete", "data": data}

    return {"intent": "unknown", "data": data}


def _extract_request(user_input: str) -> dict:
    """Extract intent/data with Gemini, falling back to local parsing offline."""
    try:
        return _model_json(user_input, _EXTRACTION_PROMPT)
    except Exception:
        return _fallback_extract(user_input)


def _fallback_reflect(intent: str, data: dict) -> dict:
    required_by_intent = {
        "add": ["title"],
        "complete": ["title"],
        "delete": ["title"],
    }
    required = required_by_intent.get(intent, [])
    missing = [field for field in required if not data.get(field)]
    return {"complete": not missing, "missing": missing}


def _reflect_extraction(intent: str, data: dict) -> dict:
    """Validate extracted data with Gemini, falling back to local rules offline."""
    extracted = {"intent": intent, "data": data}
    reflection_prompt = _REFLECTION_PROMPT.format(extracted=json.dumps(extracted))
    try:
        return _model_json(reflection_prompt)
    except Exception:
        return _fallback_reflect(intent, data)


def process_request(user_input: str) -> dict:
    """Process a task planner request and return a structured response."""
    try:
        extraction = _extract_request(user_input)
        intent = extraction.get("intent", "unknown")
        data = extraction.get("data", {})

        if "title" in data:
            data["title"] = _normalize_task_title(data["title"])

        reflection = _reflect_extraction(intent, data)
        if not reflection.get("complete", True):
            return {
                "status": "incomplete",
                "message": "Missing required fields.",
                "missing": reflection.get("missing", []),
            }

        if intent == "add":
            task_data = {
                "title": data["title"],
                "due_date": data.get("due_date", "none"),
                "status": "pending",
            }
            result = save_task(task_data)
            if result == "success":
                return {"status": "success", "message": "Task added.", "data": task_data}
            if result == "exists":
                return {"status": "exists", "message": "Task already exists.", "data": None}
            return {"status": "error", "message": "Storage error.", "data": None}

        if intent == "list":
            tasks = get_tasks()
            return {"status": "success", "message": f"{len(tasks)} task(s) found.", "data": tasks}

        if intent == "complete":
            result = complete_task(data["title"])
            if result == "success":
                return {"status": "success", "message": "Task marked complete.", "data": None}
            if result == "not_found":
                return {"status": "not_found", "message": "Task not found.", "data": None}
            return {"status": "error", "message": "Storage error.", "data": None}

        if intent == "delete":
            result = delete_task(data["title"])
            if result == "success":
                return {"status": "success", "message": "Task deleted.", "data": None}
            if result == "not_found":
                return {"status": "not_found", "message": "Task not found.", "data": None}
            return {"status": "error", "message": "Storage error.", "data": None}

        return {"status": "unknown", "message": "I can add, list, complete, or delete tasks.", "data": None}

    except Exception as exc:
        return {"status": "error", "message": str(exc), "data": None}
