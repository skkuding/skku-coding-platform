from django.urls import path

from ..views.oj import ContestAnnouncementListAPI

urlpatterns = [
    path("banner/", BannerAPI.as_view(), name="banner_api"),
]
