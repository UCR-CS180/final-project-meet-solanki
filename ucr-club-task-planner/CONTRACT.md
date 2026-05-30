# CONTRACT.md

## Purpose

This file explains how my UCR Club Task Planner is split into three layers:
`interface`, `engine`, and `storage`.

## 1) Components

- `interface`: gets user input and prints messages back to the user
- `engine`: figures out the user's intent, checks required information, and calls storage
- `storage`: reads and writes task records

## 2) Functionality: Add Task

- `interface`: collect the user's task request and show the result
- `engine`: extract the task title and due date from the request
- `storage`: check for duplicate task title and save the task

`interface -> engine`
- Function: `process_request(user_input: str) -> dict`
- Success: `{"status": "success", "message": "Task added.", "data": task_record}`
- Failure: `incomplete`, `exists`, `error`, `unknown`

`engine -> storage`
- Function: `save_task(task_data: dict) -> str`
- Input: `{"title": str, "due_date": str, "status": "pending"}`
- Success: `"success"`
- Failure: `"exists"` or `"error"`

## 3) Functionality: List Tasks

- `interface`: ask for tasks and display the task list
- `engine`: recognize the list-task request
- `storage`: return saved task records

`interface -> engine`
- Function: `process_request(user_input: str) -> dict`
- Success: `{"status": "success", "message": "2 task(s) found.", "data": [task_record, ...]}`
- Failure: `error`, `unknown`

`engine -> storage`
- Function: `get_tasks() -> list[dict]`
- Input: none
- Success: list of task records
- Failure: empty list if storage cannot be read

## 4) Functionality: Mark Task Complete

- `interface`: collect the user's complete-task request and show the result
- `engine`: extract the task title and call storage
- `storage`: find the task and change its status to `complete`

`interface -> engine`
- Function: `process_request(user_input: str) -> dict`
- Success: `{"status": "success", "message": "Task marked complete.", "data": task_record}`
- Failure: `incomplete`, `not_found`, `error`, `unknown`

`engine -> storage`
- Function: `complete_task(task_title: str) -> str`
- Input: task title
- Success: `"success"`
- Failure: `"not_found"` or `"error"`

## 5) Functionality: Delete Task

- `interface`: collect the user's delete-task request and show the result
- `engine`: extract the task title and call storage
- `storage`: find and delete the matching task

`interface -> engine`
- Function: `process_request(user_input: str) -> dict`
- Success: `{"status": "success", "message": "Task deleted.", "data": None}`
- Failure: `incomplete`, `not_found`, `error`, `unknown`

`engine -> storage`
- Function: `delete_task(task_title: str) -> str`
- Input: task title
- Success: `"success"`
- Failure: `"not_found"` or `"error"`

## 6) Boundary Rules

- The interface should not directly read or write storage.
- The storage layer should not decide what the user meant.
- The engine should be the only layer that chooses which storage function to call.
