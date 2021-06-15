"""Api app models."""
from __future__ import annotations

import json
from datetime import date

from django.db import models


class Forecast(models.Model):
    """Forecast database model."""

    date = models.DateField(db_index=True, default=date.today)
    country_code = models.CharField(max_length=2, db_index=True)

    forecast = models.CharField(max_length=10)

    class Meta:
        """Forecast model meta class."""

        constraints = [
            models.UniqueConstraint(
                fields=["date", "country_code"],
                name="date and country_code pair",
            ),
        ]

    def __str__(self) -> str:
        """Return string representation of the model."""
        return json.dumps({"forecast": self.forecast})
