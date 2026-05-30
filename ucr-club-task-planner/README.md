# UCR Club Task Planner

## What It Does

UCR Club Task Planner is a terminal app for tracking simple club tasks. It can add a task, list saved tasks, mark a task complete, and delete a task using simple commands.

## Project Files

- Source code: `src/`
- Tests: `tests/`
- Requirement/design documents: `FUNCTIONALITY.md` and `CONTRACT.md`
- Demo video: TODO add public video link before creating the GitHub release

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your Gemini API key:

```text
GOOGLE_API_KEY=your_key_here
```

For Google Sheets storage, keep `service_account.json` in the project root and share the spreadsheet with the service account email.

## How To Run

```bash
python verify_connection.py
python -m src.interface.cli
```

## How To Test

```bash
python3 -m pytest tests/ -q
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
