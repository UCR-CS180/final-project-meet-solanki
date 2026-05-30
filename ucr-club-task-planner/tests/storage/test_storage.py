from src.storage.storage_handler import save_task
from src.storage.storage_handler_extended import complete_task, delete_task, get_tasks


def test_save_new_task_success():
    sample_data = {
        "title": "finish club budget",
        "due_date": "Friday",
        "status": "pending",
    }

    result = save_task(sample_data)

    assert result == "success"


def test_duplicate_task_prevention():
    sample_data = {
        "title": "finish club budget",
        "due_date": "Friday",
        "status": "pending",
    }

    save_task(sample_data)
    result = save_task(sample_data)

    assert result == "exists"


def test_missing_fields_error():
    incomplete_data = {"title": "finish club budget"}

    result = save_task(incomplete_data)

    assert result == "error"


def test_get_tasks_returns_saved_tasks():
    save_task({"title": "email members", "due_date": "Monday", "status": "pending"})

    result = get_tasks()

    assert result == [{"title": "email members", "due_date": "Monday", "status": "pending"}]


def test_complete_task_success_and_not_found():
    save_task({"title": "email members", "due_date": "Monday", "status": "pending"})

    assert complete_task("Email Members") == "success"
    assert get_tasks()[0]["status"] == "complete"
    assert complete_task("missing task") == "not_found"


def test_complete_task_accepts_partial_title():
    save_task({
        "title": "complete meeting with everyone through zoom",
        "due_date": "Thursday",
        "status": "pending",
    })

    assert complete_task("meeting with everyone through zoom") == "success"
    assert get_tasks()[0]["status"] == "complete"


def test_delete_task_success_and_not_found():
    save_task({"title": "email members", "due_date": "Monday", "status": "pending"})

    assert delete_task("Email Members") == "success"
    assert get_tasks() == []
    assert delete_task("missing task") == "not_found"


def test_delete_task_accepts_partial_title():
    save_task({"title": "called take roll call for friday", "due_date": "none", "status": "pending"})

    assert delete_task("take roll call for friday") == "success"
    assert get_tasks() == []
