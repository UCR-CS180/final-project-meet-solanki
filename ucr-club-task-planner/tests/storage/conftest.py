"""Pytest fixtures for storage tests.

The real project uses Google Sheets, but these tests use an in-memory sheet
so they can run without touching live data.
"""

from dataclasses import dataclass

import pytest
import src.storage.storage_handler as handler
import src.storage.storage_handler_extended as extended


@dataclass
class _Cell:
    row: int
    col: int


class _InMemoryWorksheet:
    def __init__(self):
        self._rows = [["title", "due_date", "status"]]

    def col_values(self, col: int) -> list[str]:
        return [row[col - 1] for row in self._rows if len(row) >= col]

    def append_row(self, row: list) -> None:
        self._rows.append(row)

    def get_all_records(self) -> list[dict]:
        headers = self._rows[0]
        return [dict(zip(headers, row)) for row in self._rows[1:]]

    def find(self, value: str, in_column: int):
        for row_index, row in enumerate(self._rows, start=1):
            if len(row) >= in_column and row[in_column - 1].lower() == value.lower():
                return _Cell(row=row_index, col=in_column)
        return None

    def update_cell(self, row: int, col: int, value: str) -> None:
        self._rows[row - 1][col - 1] = value

    def delete_rows(self, row: int) -> None:
        del self._rows[row - 1]


@pytest.fixture(autouse=True)
def in_memory_worksheet(monkeypatch):
    ws = _InMemoryWorksheet()
    monkeypatch.setattr(handler, "_get_worksheet", lambda: ws)
    monkeypatch.setattr(extended, "_open_sheet", lambda: ws)
