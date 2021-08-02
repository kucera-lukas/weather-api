"""Test the app exceptions module."""
from __future__ import annotations

import json

import pytest

from weather_api.apps.app_forecast.exceptions import InvalidQueryParams


@pytest.mark.parametrize(
    "status_code, message, field, value",
    [(200, "exception test message", "field", "value")],
)
def test_invalid_query_params_repr(
    status_code: int,
    message: str,
    field: str,
    value: str,
) -> None:
    """Test the __repr__ method of ``InvalidQueryParams``."""
    obj = InvalidQueryParams(
        status_code=status_code,
        message=message,
        field=field,
        value=value,
    )

    assert json.loads(repr(obj)) == {"detail": message, "field": field, "value": value}
