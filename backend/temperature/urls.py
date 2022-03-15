from django.urls import path

from .views import TemperatureAPI, RankAPI

urlpatterns = [
    path("temperature/", TemperatureAPI.as_view(), name="temperature_api"),
    path("rank/", RankAPI.as_view(), name="rank_api")
]
