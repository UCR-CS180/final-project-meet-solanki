# UCR Club Task Planner

## What It Does

UCR Club Task Planner is a terminal app for tracking simple club tasks. It can add a task, list saved tasks, mark a task complete, and delete a task using simple commands.

## Project Files

| Path | Description |
| --- | --- |
| `src/` | Source code directory |
| `tests/` | Test directory |
| `FUNCTIONALITY.md` | Requirement specification |
| `CONTRACT.md` | Design document with component contracts |

## Demo Video

https://drive.google.com/file/d/1dBnb8GxUDdGqIZK52vLNNxlwnS4jZ1JG/view?usp=sharing

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local `.env` file:

```text
GOOGLE_API_KEY=your_key_here
SPREADSHEET_NAME=ucr-club-task-planner
```

Keep `service_account.json` in this project folder and share the Google Sheet with the service account email.

## How To Run

```bash
python verify_connection.py
python -m src.interface.cli
```

## How To Test

```bash
python -m pytest tests/ -q
```

## Usage Examples

Input:

```text
Add a task to finish club budget by Friday.
```

Expected output:

```text
Task added.
```

Input:

```text
Show my club tasks.
```

Expected output:

```text
1 task(s) found.
  - finish club budget (pending, due Friday)
```

Input:

```text
Mark finish club budget complete.
```

Expected output:

```text
Task marked complete.
```
