"""Command-line interface for the UCR Club Task Planner."""

from __future__ import annotations

from src.engine.engine import process_request

_WELCOME_BANNER = """
========================================
  UCR Club Task Planner
  Type 'quit' or 'exit' to stop.
========================================
"""

_HELP_TEXT = (
    "I can help you:\n"
    "  - Add a task\n"
    "  - List tasks\n"
    "  - Mark a task complete\n"
    "  - Delete a task"
)


def format_response(result: dict) -> str:
    """Turn an engine result dictionary into text for the terminal."""
    status = result.get("status")
    message = result.get("message", "Unexpected response.")

    if status == "success":
        lines = [message]
        data = result.get("data")
        if isinstance(data, list):
            for task in data:
                lines.append(
                    f"  - {task.get('title')} ({task.get('status')}, due {task.get('due_date')})"
                )
        return "\n".join(lines)

    if status in {"exists", "not_found"}:
        return message

    if status == "incomplete":
        missing = ", ".join(result.get("missing", []))
        return f"{message}\n  Missing: {missing}"

    if status == "unknown":
        return f"{message}\n\n{_HELP_TEXT}"

    return message


def run_session(process_fn=None) -> None:
    """Run the terminal chat loop."""
    if process_fn is None:
        process_fn = process_request

    print(_WELCOME_BANNER)

    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            print("Goodbye!")
            return

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            return

        result = process_fn(user_input)
        print(f"Assistant: {format_response(result)}")
        print()


if __name__ == "__main__":
    run_session()
