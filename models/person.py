from __future__ import annotations
import re
from typing import Pattern


class Person:
    """Base class for any person-like entity in the system."""

    _email_pattern: Pattern[str] = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, name: str, email: str) -> None:
        """Initialize a person with a name and validated email."""
        self.name = name
        self.email = email

    @property
    def name(self) -> str:
        """Get the person's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the person's name with basic normalization."""
        self._name = value.strip()

    @property
    def email(self) -> str:
        """Get the person's email address."""
        return self._email

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Return whether the supplied email matches a simple validation pattern."""
        return bool(Person._email_pattern.match(email))

    @email.setter
    def email(self, value: str) -> None:
        """Set the person's email after validating the format."""
        normalized = value.strip().lower()
        if not self._validate_email(normalized):
            raise ValueError(f"Invalid email address: {value}")
        self._email = normalized

    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"{self.name} <{self.email}>"
