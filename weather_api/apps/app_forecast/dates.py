"""Parse/format string/datetime objects."""
from __future__ import annotations

import functools as fn
from datetime import datetime, date


@fn.lru_cache(maxsize=10)
def date_to_api_format(dt: date, /) -> str:
    """Return a date in ``WeatherAPI`` datetime format.

    :param dt: The ``Date`` object to convert

    """
    return str(dt.strftime("%Y-%m-%d"))


@fn.lru_cache(maxsize=10)
def api_str_to_date(dt: str, /) -> date:
    """Return string converted from api request to a ``date`` object.

    :param dt: The string to convert

    :raises ValueError: if given date is invalid

    """
    parsed_date = datetime.strptime(dt, "%Y-%m-%d").date()

    if not validate_date(parsed_date):
        raise ValueError(f"date is not valid")

    return parsed_date


def validate_date(dt: date, /) -> bool:
    """Validate a date provided by a user.

    :param dt: Date to validate

    """
    now = date.today()
    return dt > now


def days_in_advance(dt: date, /) -> int:
    """Return how many days are there between now and the given date.

    :param dt: The date to check

    """
    now = date.today()
    delta = dt - now
    return delta.days + 1
