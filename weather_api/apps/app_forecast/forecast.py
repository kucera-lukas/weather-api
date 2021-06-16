"""Main logic behind retrieving information about weather."""
from __future__ import annotations

import functools as fn
from contextlib import suppress
from typing import TYPE_CHECKING, Any, Iterator

import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from . import database, dates
from .constants import API_URL, COUNTRY_CITIES
from .exceptions import InvalidQueryParams

if TYPE_CHECKING:
    from datetime import date as TDate

    from .models import Forecast


def main(date: str, country_code: str) -> Forecast:
    """Return simple weather forecast.

    :param date: Date of wanted weather forecast
    :param country_code: Country code of the wanted country

    :raises InvalidQueryParams: if some user input is wrong
    :raises HTTPError: if something goes wrong with ``WeatherAPI`` request

    """
    try:
        parsed_date = dates.api_str_to_date(date)
    except ValueError as e:
        raise InvalidQueryParams(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=e.args[0],
            field="date",
            value=date,
        ) from e

    with suppress(ObjectDoesNotExist):
        obj = database.get(date=parsed_date, country_code=country_code)
        return obj

    try:
        city = get_city(country_code=country_code)
    except ValueError as e:
        raise InvalidQueryParams(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=e.args[0],
            field="country_code",
            value=country_code,
        ) from e

    days = dates.days_in_advance(parsed_date)
    response = get_response(city=city, days=days)
    try:
        avg_temp = average_temperature(response=response, request_date=parsed_date)
    except ValueError as e:
        raise InvalidQueryParams(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=f"our internal weather provider does not have forecast data about the date {date!r}",
            field="date",
            value=date,
        ) from e
    result = get_simple_forecast(avg_temp=avg_temp)

    forecast = database.create(
        date=parsed_date,
        country_code=country_code,
        result=result,
    )
    return forecast


def get_city(country_code: str) -> str:
    """Return a country capital city.

    :param country_code: Code of the wanted country

    :raises ValueError: if given ``country_code`` is not in ``COUNTRY_CITIES`` dict

    """
    try:
        city = COUNTRY_CITIES[country_code]
    except KeyError as e:
        raise ValueError("country code is not valid") from e
    return city


def get_response(city: str, days: int) -> dict[str, Any]:
    """Return a WeatherAPI response.

    :param city: City
    :param days: How many days in advance we need to request

    :raises HTTPError: if something goes wrong with the api request

    """
    response = requests.get(f"{API_URL}&q={city}&days={days}")
    response.raise_for_status()
    return response.json()


def average_temperature(response: dict, request_date: TDate) -> float:
    """Return average temperature from a ``WeatherAPI`` response.

    :param response: The ``WeatherAPI`` response
    :param request_date: Requested prediction date

    :raises ValueError: if the response can't be correctly read

    """
    api_date = dates.date_to_api_format(request_date)
    forecast_day: list[dict[str, Any]] = response["forecast"]["forecastday"]

    request_filter: Iterator[float] = (
        forecast["day"]["avgtemp_c"]
        for forecast in forecast_day
        if forecast["date"] == api_date
    )

    try:
        result = next(request_filter)
    except StopIteration as e:
        raise ValueError("Could not find given date in WeatherAPI response") from e
    return result


@fn.lru_cache(maxsize=None, typed=True)
def get_simple_forecast(avg_temp: float) -> str:
    """Return a simple forecast representation.

    :param avg_temp: Average temperature of the day forecast to simplify

    """
    if avg_temp >= 20:
        output = "good"
    elif avg_temp >= 10:
        output = "soso"
    else:
        output = "bad"
    return output
