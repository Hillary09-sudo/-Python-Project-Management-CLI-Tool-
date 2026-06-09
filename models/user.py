from __future__ import annotations
from typing import Any
from .person import Person


class User(Person):
    """Represents a user with an optional list of owned project IDs."""

    NEXT_ID = 1

    def __init__(self, name: str, email: str, user_id: int | None = None, project_ids: list[int] | None = None) -> None:
        """Initialize a user, optionally using an existing ID and project associations."""
        super().__init__(name, email)
        self.id = user_id if user_id is not None else User._generate_id()
        self.project_ids = project_ids or []

    @classmethod
    def _generate_id(cls) -> int:
        """Generate a unique incremental user ID."""
        current = cls.NEXT_ID
        cls.NEXT_ID += 1
        return current

    def to_dict(self) -> dict[str, Any]:
        """Serialize the user to a dictionary for JSON persistence."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "project_ids": self.project_ids,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "User":
        """Create a User instance from a persisted dictionary."""
        user = cls(
            name=payload["name"],
            email=payload["email"],
            user_id=payload.get("id"),
            project_ids=payload.get("project_ids", []),
        )
        cls.NEXT_ID = max(cls.NEXT_ID, user.id + 1)
        return user

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"
