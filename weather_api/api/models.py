"""Api app models."""
from django.db import models


class Forecast(models.Model):
    """Forecast database model."""

    date = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=2)

    result = models.CharField(max_length=10)