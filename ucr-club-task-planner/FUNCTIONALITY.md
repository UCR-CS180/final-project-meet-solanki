# FUNCTIONALITY.md

## Purpose

My project is a UCR club task planner. The goal is to help a club member keep track of simple tasks.

## Functionality 1: Add Task

- Input:
  - A simple request, for example: "Add a task to finish the club budget by Friday."
- Output:
  - A message saying whether the task was saved.
- Success:
  - The task has a title and is saved with status `pending`.
- Failure/Edge Cases:
  - Missing task title -> return `incomplete`
  - Duplicate task title -> return `exists`
  - Storage problem -> return `error`

## Functionality 2: List Tasks

- Input:
  - A request like: "Show my club tasks."
- Output:
  - A list of saved tasks with their due date and status.
- Success:
  - The system returns all saved tasks.
- Failure/Edge Cases:
  - No tasks saved yet -> return an empty list
  - Storage problem -> return `error`

## Functionality 3: Mark Task Complete

- Input:
  - A request like: "Mark finish club budget complete."
- Output:
  - A message saying whether the task was updated.
- Success:
  - The matching task status changes to `complete`.
- Failure/Edge Cases:
  - Missing task title -> return `incomplete`
  - Task is not found -> return `not_found`
  - Storage problem -> return `error`

## Functionality 4: Delete Task

- Input:
  - A request like: "Delete finish club budget."
- Output:
  - A message saying whether the task was deleted.
- Success:
  - The matching task is removed from storage.
- Failure/Edge Cases:
  - Missing task title -> return `incomplete`
  - Task is not found -> return `not_found`
  - Storage problem -> return `error`
