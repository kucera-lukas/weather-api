"""Api app models."""
from __future__ import annotations

import json

from django.db import models


class Forecast(models.Model):
    """Forecast database model."""

    date = models.DateField(auto_now_add=True, unique=True)
    country_code = models.CharField(max_length=2)

    forecast = models.CharField(max_length=10)

    def __str__(self) -> str:
        """Return string representation of the model."""
        return json.dumps({"forecast": self.forecast})
