"""App database query interface."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .models import Forecast

if TYPE_CHECKING:
    from datetime import date as Tdate


def get(date: Tdate, country_code: str) -> Forecast:
    """Return an existing Forecast object or None.

    :param date: Date of the wanted entry
    :param country_code: Country code of the wanted entry

    :raises DoesNotExist: if the wanted entry does not exist

    """
    obj = Forecast.objects.get(date=date, country_code=country_code)
    return obj


def create(country_code: str, result: str) -> Forecast:
    """Create a new entry in Forecast table.

    :param country_code: Country code of the new entry
    :param result: Weather forecast for the new entry

    """
    obj = Forecast(country_code=country_code, result=result)
    obj.save()
    return obj
