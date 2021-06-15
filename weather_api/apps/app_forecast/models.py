"""Api app models."""
from django.db import models


class Forecast(models.Model):
    """Forecast database model."""

    date = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=2)

    forecast = models.CharField(max_length=10)

    def __str__(self) -> str:
        """Return string representation of the model."""
        return str(self.forecast)
