from django.urls import path

from ..views import JudgeServerHeartbeatAPI, LanguagesAPI, WebsiteConfigAPI

urlpatterns = [
    path("website/", WebsiteConfigAPI.as_view(), name="website_info_api"),
    path("judge_server_heartbeat/", JudgeServerHeartbeatAPI.as_view(), name="judge_server_heartbeat_api"),
    path("languages/", LanguagesAPI.as_view(), name="language_list_api")
]
