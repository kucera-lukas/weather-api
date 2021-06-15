"""Django app_forecast app urls."""
from django.urls import path

from .views import forecast_endpoint

urlpatterns = [
    path("", forecast_endpoint),
]
