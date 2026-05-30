"""Unit tests for the task planner engine layer."""

from unittest.mock import patch

from src.engine.engine import process_request


def test_add_task_success_returns_correct_status():
    with patch("src.engine.engine.save_task", return_value="success"):
        result = process_request("Add a task to finish club budget by Friday.")

    assert result["status"] == "success"
    assert "message" in result


def test_add_task_duplicate_returns_exists_status():
    with patch("src.engine.engine.save_task", return_value="exists"):
        result = process_request("Add a task to finish club budget by Friday.")

    assert result["status"] == "exists"
    assert "message" in result


def test_list_tasks_returns_success_with_data():
    mock_tasks = [{"title": "finish club budget", "due_date": "Friday", "status": "pending"}]
    with patch("src.engine.engine.get_tasks", return_value=mock_tasks):
        result = process_request("Show my club tasks.")

    assert result["status"] == "success"
    assert isinstance(result["data"], list)


def test_incomplete_add_task_is_blocked_before_storage():
    with patch("src.engine.engine.save_task") as mock_save:
        result = process_request("Add a task.")

    assert result["status"] == "incomplete"
    assert "missing" in result
    mock_save.assert_not_called()


def test_complete_task_success_returns_correct_status():
    with patch("src.engine.engine.complete_task", return_value="success") as mock_complete:
        result = process_request("Mark task finish club budget complete.")

    assert result["status"] == "success"
    mock_complete.assert_called_once_with("finish club budget")


def test_complete_task_accepts_task_called_phrase():
    with patch("src.engine.engine.complete_task", return_value="success") as mock_complete:
        result = process_request("Mark task called take roll call for friday complete.")

    assert result["status"] == "success"
    mock_complete.assert_called_once_with("called take roll call for friday")


def test_delete_task_success_returns_correct_status():
    with patch("src.engine.engine.delete_task", return_value="success") as mock_delete:
        result = process_request("Delete task finish club budget.")

    assert result["status"] == "success"
    mock_delete.assert_called_once_with("finish club budget")


def test_unknown_intent_returns_unknown_status():
    result = process_request("What is the meaning of life?")

    assert result["status"] == "unknown"
    assert "message" in result
