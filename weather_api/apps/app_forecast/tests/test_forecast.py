"""Test the app forecast module."""
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pytest

from weather_api.apps.app_forecast import forecast

if TYPE_CHECKING:
    from pytest_mock import MockFixture


def test_get_response(mocker: MockFixture) -> None:
    """Test the get_response function."""
    return_obj = type(
        "return_object",
        tuple(),
        {
            "get": lambda: {"return_value": "test"},
            "raise_for_status": lambda: "OK",
            "json": lambda: {"return_value": "test_json"},
        },
    )
    requests_get = mocker.patch("requests.get", return_value=return_obj)

    result = forecast.get_response(city="Prague", days=10)

    requests_get.assert_called_once()
    assert result == {"return_value": "test_json"}


def test_average_temperature(mocker: MockFixture) -> None:
    """Tets the average_temperature function."""
    api_format = mocker.patch(
        "weather_api.apps.app_forecast.dates.date_to_api_format",
        return_value="2000-01-01",
    )
    avg_temp = 20
    test_response = {
        "forecast": {
            "forecastday": [{"date": "2000-01-01", "day": {"avgtemp_c": avg_temp}}],
        },
    }

    request_date = date(2000, 1, 1)
    result = forecast.average_temperature(
        response=test_response,
        request_date=request_date,
    )

    api_format.assert_called_once_with(request_date)
    assert result == avg_temp


def test_average_temperature_raises(mocker: MockFixture) -> None:
    """Tets that the average_temperature function raises error if nothing found."""
    api_format = mocker.patch(
        "weather_api.apps.app_forecast.dates.date_to_api_format",
        return_value="2000-01-01",
    )
    avg_temp = 20
    test_response = {
        "forecast": {
            "forecastday": [{"date": "3000-01-01", "day": {"avgtemp_c": avg_temp}}],
        },
    }

    request_date = date(2000, 1, 1)

    with pytest.raises(ValueError):
        forecast.average_temperature(response=test_response, request_date=request_date)
    api_format.assert_called_once_with(request_date)


@pytest.mark.parametrize(
    "country_code, city",
    [("CZ", "Prague"), ("SK", "Bratislava"), ("UK", "London")],
)
def test_get_city(country_code: str, city: str) -> None:
    """Test the get_city function."""
    result = forecast.get_city(country_code)

    assert result == city


@pytest.mark.parametrize(
    "country_code, city",
    ["XX", "US", "CA"],
)
def test_get_city_raises(country_code: str, city: str) -> None:
    """Test that get_city function raises if invalid code is passed in."""
    with pytest.raises(ValueError):
        forecast.get_city(country_code)


@pytest.mark.parametrize(
    "temperature, expected",
    [(25, "good"), (15, "soso"), (5, "bad")],
)
def test_get_simple_forecast(temperature: int, expected: str) -> None:
    """Test the get_simple_forecast function."""
    result = forecast.get_simple_forecast(avg_temp=temperature)

    assert result == expected


def test_get_simple_forecast_cached() -> None:
    """Test that get_simple_forecast function caches results."""
    forecast.get_simple_forecast.cache_clear()
    temperature = 25.5

    assert forecast.get_simple_forecast.cache_info().hits == 0
    forecast.get_simple_forecast(temperature)
    assert forecast.get_simple_forecast.cache_info().misses == 1
    forecast.get_simple_forecast(temperature)
    assert forecast.get_simple_forecast.cache_info().hits == 1
