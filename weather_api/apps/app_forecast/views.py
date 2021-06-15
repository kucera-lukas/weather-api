"""App views."""
from __future__ import annotations

from requests import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import forecast


@api_view(http_method_names=["GET"])
def forecast_endpoint(request) -> Response:
    """Weather forecast endpoint.

    Query params:
        date str: Date of wanted weather forecast with %Y-%m-%d
        country_code str: Code of the country for which to get forecast
            see constants.py for available codes
    """
    try:
        date = request.query_params["date"]
        country_code = request.query_params["country_code"]
    except KeyError:
        return Response(
            data="please enter all required query params",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        result = forecast.api(
            date=date,
            country_code=country_code,
        )
    except ValueError as e:
        return Response(
            data=f"invalid query params -> {e.args}",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except HTTPError:
        return Response(
            data="something went wrong, sorry...",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(data=result, status=status.HTTP_200_OK)
