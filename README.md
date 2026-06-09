# UCR Club Task Planner

UCR Club Task Planner is a terminal-based assistant for tracking simple club tasks. It can add tasks, list saved tasks, mark tasks complete, and delete tasks using plain English commands.

## Project Paths

| Path | Description |
| --- | --- |
| `ucr-club-task-planner/src/` | Source code directory |
| `ucr-club-task-planner/tests/` | Test directory |
| `ucr-club-task-planner/FUNCTIONALITY.md` | Requirement specification |
| `ucr-club-task-planner/CONTRACT.md` | Design document with component contracts |

## Demo Video

https://drive.google.com/file/d/1dBnb8GxUDdGqIZK52vLNNxlwnS4jZ1JG/view?usp=sharing

## Setup

### Prerequisites

- Python 3.10+
- A Gemini API key
- A Google Cloud service account with access to the target Google Sheet
- A Google Sheet named `ucr-club-task-planner` with this header row:

```text
title    due_date    status
```

### Install Dependencies

```bash
cd ucr-club-task-planner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The project requires:

```text
pytest>=8.0.0
gspread>=6.0.0
google-auth>=2.0.0
google-genai>=1.0.0
python-dotenv>=1.0.0
pytest-cov>=4.0.0
```

### Local Credentials

Create a local `.env` file inside `ucr-club-task-planner/`:

```text
GOOGLE_API_KEY=your_key_here
SPREADSHEET_NAME=ucr-club-task-planner
```

Place your Google service account credentials in:

```text
ucr-club-task-planner/service_account.json
```

These credential files are intentionally ignored by Git and should not be committed.

## Running the Assistant

```bash
cd ucr-club-task-planner
source .venv/bin/activate
python verify_connection.py
python -m src.interface.cli
```

Example commands:

```text
Add a task to finish club budget by Friday.
Show my club tasks.
Mark finish club budget complete.
Delete finish club budget.
quit
```

## Running Tests

```bash
cd ucr-club-task-planner
source .venv/bin/activate
python -m pytest tests/ -q
```
