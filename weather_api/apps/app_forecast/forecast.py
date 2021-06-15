"""Main logic behind retrieving information about weather."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

import requests

from . import dates
from .constants import COUNTRY_CITIES, API_URL

if TYPE_CHECKING:
    from datetime import date as TDate


def api(date: str, country_code: str) -> dict[str, str]:
    """Return simple weather forecast.

    :param date: Date of wanted weather forecast
    :param country_code: Country code of the wanted country

    :raises ValueError: if some user input is wrong
    :raises HTTPError: if something goes wrong with ``WeatherAPI`` request

    """
    city = get_city(country_code=country_code)
    parsed_date = dates.api_str_to_date(date)
    days = dates.days_in_advance(parsed_date)
    response = get_response(city=city, days=days)
    avg_temp = average_temperature(response=response, request_date=parsed_date)
    return get_simple_forecast(avg_temp=avg_temp)


def get_city(country_code: str) -> str:
    """Return a country capital city.

    :param country_code: Code of the wanted country

    :raises ValueError: if given ``country_code`` is not in ``COUNTRY_CITIES`` dict

    """
    try:
        city = COUNTRY_CITIES[country_code]
    except KeyError as e:
        raise ValueError(f"Country code {country_code!r} is not valid") from e
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


def get_simple_forecast(avg_temp: float) -> dict[str, str]:
    """Return a simple forecast representation.

    :param avg_temp: Average temperature of the day forecast to simplify

    """
    if avg_temp >= 20:
        output = "good"
    elif avg_temp >= 10:
        output = "soso"
    else:
        output = "bad"
    return {"forecast": output}
