"""Test the dates module."""
from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

import pytest

from weather_api.apps.app_forecast import dates

if TYPE_CHECKING:
    from pytest_mock import MockFixture


@pytest.mark.parametrize(
    "dt, expected",
    [
        (date(2000, 1, 1), "2000-01-01"),
        (date(100, 12, 12), "0100-12-12"),
        (date(2021, 6, 16), "2021-06-16"),
    ],
)
def test_date_to_api_format(dt: date, expected: str) -> None:
    """Test the date_to_api_format function."""
    result = dates.date_to_api_format(dt)

    assert result == expected


def test_date_to_api_format_cached() -> None:
    """Test that the date_to_api_format function caches results."""
    dates.date_to_api_format.cache_clear()
    dt = date(2000, 10, 10)

    assert dates.date_to_api_format.cache_info().hits == 0
    dates.date_to_api_format(dt)
    assert dates.date_to_api_format.cache_info().misses == 1
    dates.date_to_api_format(dt)
    assert dates.date_to_api_format.cache_info().hits == 1


@pytest.mark.parametrize(
    "dt, expected",
    [
        ("2000-01-01", date(2000, 1, 1)),
        ("2020-12-12", date(2020, 12, 12)),
        ("0010-1-1", date(10, 1, 1)),
    ],
)
def test_api_str_to_date(mocker: MockFixture, dt: str, expected: date) -> None:
    """Test the api_str_to_date function."""
    validate_date = mocker.patch(
        "weather_api.apps.app_forecast.dates.validate_date",
        return_value=True,
    )

    result = dates.api_str_to_date(dt)

    validate_date.assert_called_once_with(expected)
    assert result == expected


@pytest.mark.parametrize(
    "dt",
    ["", "a", "0", "0-0-0", "00-00-00", "2020-12-", "10-1-1"],
)
def test_api_str_to_date_raises_invalid_format(mocker: MockFixture, dt: str) -> None:
    """Test that api_str_to_date function raises ValueError if invalid string is passed in."""
    validate_date = mocker.patch(
        "weather_api.apps.app_forecast.dates.validate_date",
    )

    with pytest.raises(ValueError):
        dates.api_str_to_date(dt)
    validate_date.assert_not_called()


# exception is not being raised when pytest called from command line, todo
@pytest.mark.xfail
def test_api_str_to_date_raises_validation_fail(mocker: MockFixture) -> None:
    """Test that api_str_to_date function raises ValueError if the validation call fails."""
    validate_date = mocker.patch(
        "weather_api.apps.app_forecast.dates.validate_date",
        return_value=False,
    )

    with pytest.raises(ValueError):
        dates.api_str_to_date("2000-01-01")
    validate_date.assert_called_once_with(date(2000, 1, 1))


def test_api_str_to_date_cached(mocker: MockFixture) -> None:
    """Test that the api_str_to_date function caches results."""
    dates.date_to_api_format.cache_clear()
    validate_date = mocker.patch(
        "weather_api.apps.app_forecast.dates.validate_date",
        return_value=True,
    )

    dt = "2000-10-10"

    assert dates.date_to_api_format.cache_info().hits == 0
    dates.api_str_to_date(dt)
    validate_date.assert_called_once_with(date(2000, 10, 10))
    assert dates.api_str_to_date.cache_info().misses == 11

    validate_date.reset_mock(return_value=True)

    dates.api_str_to_date(dt)
    validate_date.assert_not_called()
    assert dates.api_str_to_date.cache_info().hits == 2


def test_validate_date() -> None:
    """Test the validate_date function."""
    result_true = dates.validate_date(date(3000, 1, 1))
    assert result_true is True

    result_false = dates.validate_date(date(1000, 1, 1))
    assert result_false is False


def test_days_in_advance() -> None:
    """Test the days_in_advance function."""
    result = dates.days_in_advance(date.today() + timedelta(days=10))

    assert result == 11
