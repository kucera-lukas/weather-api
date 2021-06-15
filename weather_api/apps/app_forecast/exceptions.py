"""App exception."""
from __future__ import annotations

import json


class InvalidQueryParams(Exception):
    """Raised when invalid query params are passed into an api endpoint."""

    def __init__(self, status_code: int, message: str, field: str, value: str) -> None:
        """Construct the class."""
        self.status_code = status_code
        self.message = message
        self.field = field
        self.value = value

    def __repr__(self) -> str:
        """Return information about this class."""
        return json.dumps(
            {"detail": self.message, "field": self.field, "value": self.value},
        )
