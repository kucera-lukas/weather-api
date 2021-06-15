"""Django app constants."""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# no trailing comma because we would get tuple instead of str
API_URL = (
    f"https://api.weatherapi.com/v1/forecast.json?key={os.environ['WEATHER_API_KEY']}"
)

COUNTRY_CODES = ("CZ", "SK", "UK")
COUNTRY_CITIES = dict(zip(COUNTRY_CODES, ("Prague", "Bratislava", "London")))
