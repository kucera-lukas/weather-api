"""Weather-forecast django management command."""
from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from requests import HTTPError

from ... import forecast
from ...exceptions import InvalidQueryParams


class Command(BaseCommand):
    """Management command for the forecast app."""

    help = "Return simplified information about weather forecast."

    def add_arguments(self, parser):
        """Add arguments to the command."""
        parser.add_argument(
            "date",
            type=str,
            help="Date of the wanted weather forecast info",
        )
        parser.add_argument(
            "country_code",
            type=str,
            help="Country code for weather forecast info",
        )

    def handle(self, *args, **kwargs):
        """Handle a command."""
        try:
            result = forecast.main(
                date=kwargs["date"],
                country_code=kwargs["country_code"],
            )
        except InvalidQueryParams as e:
            raise CommandError(e.message)
        # if WeatherAPI request fails
        except HTTPError:
            raise CommandError(message="something went wrong, sorry...")

        self.stdout.write(msg=self.style.SUCCESS(result))
