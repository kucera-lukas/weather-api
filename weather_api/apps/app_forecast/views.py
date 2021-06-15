"""App views."""
from __future__ import annotations

import json

from requests import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import forecast
from .exceptions import InvalidQueryParams


@api_view(http_method_names=["GET"])
def forecast_endpoint(request) -> Response:
    """Weather forecast endpoint.

    Query params:
        date: Date of wanted weather forecast in %Y-%m-%d format
        country_code: Code of the country for which to get forecast

    """
    try:
        date = request.query_params["date"]
        country_code = request.query_params["country_code"]
    except KeyError:
        return Response(
            data={"detail": "please enter all required query params"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        result = forecast.api(
            date=date,
            country_code=country_code,
        )
    except InvalidQueryParams as e:
        return Response(
            data=json.loads(repr(e)),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except HTTPError:
        return Response(
            data={"detail": "something went wrong, sorry..."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(data=json.loads(str(result)), status=status.HTTP_200_OK)
