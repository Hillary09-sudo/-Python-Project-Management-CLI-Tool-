from __future__ import annotations
from datetime import datetime
import re


def validate_email(email: str) -> bool:
    """Return True if the supplied string is a valid email address."""
    if not isinstance(email, str):
        return False
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()))


def parse_date(value: str) -> str:
    """Parse a date string in YYYY-MM-DD format and return the normalized string."""
    if not isinstance(value, str):
        raise ValueError("Date value must be a string")
    try:
        parsed = datetime.strptime(value.strip(), "%Y-%m-%d")
        return parsed.date().isoformat()
    except ValueError as exc:
        raise ValueError("Date must be in YYYY-MM-DD format") from exc
