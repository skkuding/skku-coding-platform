from django.urls import path

from ..views.admin import ContestAnnouncementAPI, ContestAPI, DownloadContestSubmissions

urlpatterns = [
    path("banner/", BannerAPI.as_view(), name="banner_admin_api"),
]