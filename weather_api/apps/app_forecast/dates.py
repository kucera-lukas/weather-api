"""Parse/format string/datetime objects."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from datetime import date


def date_to_api_format(dt: date, /) -> str:
    """Return a date in ``WeatherAPI`` datetime format.

    :param dt: The ``Date`` object to convert

    """
    return str(dt.strftime("%Y-%m-%d"))


def api_str_to_date(dt: str, /) -> date:
    """Return string converted from api request to a ``date`` object.

    :param dt: The string to convert

    """
    parsed_date = datetime.strptime(dt, "%d-%m-%Y").date()
    return parsed_date


def validate_date(dt: date, /) -> bool:
    """Validate a date provided by a user.

    :param dt: Date to validate

    """
    now = datetime.now()
    return dt > now
