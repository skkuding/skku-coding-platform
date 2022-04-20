from django.urls import path

from .views import TemperatureAPI, RankAPI, TemperatureListAPI, SolvedProblemListAPI, RankListAPI

urlpatterns = [
    path("temperature/", TemperatureAPI.as_view(), name="temperature_api"),
    path("rank/", RankAPI.as_view(), name="rank_api"),
    path("profile_temperatures/", TemperatureListAPI.as_view(), name="profile_temperature_list_api"),
    path("profile_solvedproblems/", SolvedProblemListAPI.as_view(), name="profile_solvedproblems_list_api"),
    path("profile_ranks/", RankListAPI.as_view(), name="profile_rank_list_api")
]
