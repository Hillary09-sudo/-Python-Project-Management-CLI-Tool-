from __future__ import annotations
from datetime import datetime
from typing import Any


class Project:
    """Represents a project owned by a user."""

    NEXT_ID = 1

    def __init__(self, title: str, description: str, due_date: str, owner_id: int, project_id: int | None = None, task_ids: list[int] | None = None) -> None:
        """Initialize a project with title, owner, and due date validation."""
        self.id = project_id if project_id is not None else Project._generate_id()
        self.title = title.strip()
        self.description = description.strip()
        self.due_date = due_date
        self.owner_id = owner_id
        self.task_ids = task_ids or []

    @classmethod
    def _generate_id(cls) -> int:
        """Generate a unique incremental project ID."""
        current = cls.NEXT_ID
        cls.NEXT_ID += 1
        return current

    @property
    def due_date(self) -> str:
        """Get the due date string."""
        return self._due_date

    @due_date.setter
    def due_date(self, value: str) -> None:
        """Validate and set the due date in ISO format."""
        try:
            parsed = datetime.strptime(value.strip(), "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("due_date must be in YYYY-MM-DD format") from exc
        self._due_date = parsed.date().isoformat()

    def add_task(self, task_id: int) -> None:
        """Associate a task with this project."""
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)

    def is_overdue(self) -> bool:
        """Return whether the project is overdue relative to today."""
        return datetime.now().date().isoformat() > self.due_date

    def to_dict(self) -> dict[str, Any]:
        """Serialize the project for JSON persistence."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner_id": self.owner_id,
            "task_ids": self.task_ids,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Project":
        """Restore a Project instance from persisted data."""
        project = cls(
            title=payload["title"],
            description=payload["description"],
            due_date=payload["due_date"],
            owner_id=payload["owner_id"],
            project_id=payload.get("id"),
            task_ids=payload.get("task_ids", []),
        )
        cls.NEXT_ID = max(cls.NEXT_ID, project.id + 1)
        return project

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Project(id={self.id}, title={self.title!r}, owner_id={self.owner_id})"
