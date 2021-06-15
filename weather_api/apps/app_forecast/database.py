"""App database query interface."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date as Tdate

    from .models import Forecast


def get(date: Tdate, country_code: str) -> Forecast:
    """Return an existing Forecast object or None.

    :param date: Date of the wanted entry
    :param country_code: Country code of the wanted entry

    :raises DoesNotExist: if the wanted entry does not exist

    """
    from .models import Forecast

    obj = Forecast.objects.get(date=date, country_code=country_code)
    return obj


def create(date: Tdate, country_code: str, result: str) -> Forecast:
    """Create a new entry in Forecast table.

    :param date: Date of the new entry
    :param country_code: Country code of the new entry
    :param result: Weather forecast for the new entry

    """
    from .models import Forecast

    obj = Forecast(date=date, country_code=country_code, forecast=result)
    obj.save()
    return obj
