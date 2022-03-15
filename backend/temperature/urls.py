from django.urls import path

from .views import TemperatureAPI

urlpatterns = [
    path("temperature/", TemperatureAPI.as_view(), name="temperature_api")
]
