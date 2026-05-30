from src.interface.cli import format_response, run_session


def test_format_success_with_task_list_shows_title_and_status():
    result = {
        "status": "success",
        "message": "2 task(s) found.",
        "data": [
            {"title": "finish budget", "due_date": "Friday", "status": "pending"},
            {"title": "email members", "due_date": "Monday", "status": "complete"},
        ],
    }

    output = format_response(result)

    assert "finish budget" in output
    assert "pending" in output
    assert "email members" in output


def test_format_exists_shows_duplicate_message():
    result = {"status": "exists", "message": "Task already exists.", "data": None}

    output = format_response(result)

    assert "already exists" in output


def test_format_incomplete_lists_missing_fields():
    result = {"status": "incomplete", "message": "Missing required fields.", "missing": ["title"]}

    output = format_response(result)

    assert "title" in output


def test_format_unknown_includes_help_text():
    result = {
        "status": "unknown",
        "message": "I can add, list, complete, or delete tasks.",
        "data": None,
    }

    output = format_response(result)

    assert "add" in output.lower()
    assert "list" in output.lower()


def test_run_session_prints_formatted_engine_response(monkeypatch, capsys):
    def mock_engine(user_input):
        return {"status": "success", "message": "Task added.", "data": None}

    inputs = iter(["Add a task to finish budget by Friday.", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_session(process_fn=mock_engine)

    captured = capsys.readouterr()
    assert "Task added." in captured.out
