from __future__ import annotations
from typing import Any


class Task:
    """Represents a task assigned to a project and one or more contributors."""

    STATUS_CHOICES = {"pending", "in progress", "completed"}
    NEXT_ID = 1

    def __init__(self, title: str, project_id: int, assigned_to: list[int] | None = None, status: str = "pending", task_id: int | None = None) -> None:
        """Initialize a task with a title, project association, and status validation."""
        self.id = task_id if task_id is not None else Task._generate_id()
        self.title = title.strip()
        self.project_id = project_id
        self.assigned_to = assigned_to or []
        self.status = status

    @classmethod
    def _generate_id(cls) -> int:
        """Generate a unique incremental task ID."""
        current = cls.NEXT_ID
        cls.NEXT_ID += 1
        return current

    @property
    def status(self) -> str:
        """Get the current task status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Validate and set the task status."""
        normalized = value.strip().lower()
        if normalized not in self.STATUS_CHOICES:
            raise ValueError(f"Status must be one of: {', '.join(sorted(self.STATUS_CHOICES))}")
        self._status = normalized

    def complete(self) -> None:
        """Mark the task as completed."""
        self.status = "completed"

    def to_dict(self) -> dict[str, Any]:
        """Serialize the task for JSON persistence."""
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Task":
        """Restore a Task instance from persisted data."""
        task = cls(
            title=payload["title"],
            project_id=payload["project_id"],
            assigned_to=payload.get("assigned_to", []),
            status=payload.get("status", "pending"),
            task_id=payload.get("id"),
        )
        cls.NEXT_ID = max(cls.NEXT_ID, task.id + 1)
        return task

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"
