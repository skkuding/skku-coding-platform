from django.urls import path

from ..views.oj import AnnouncementAPI, AnnouncementDetailAPI

urlpatterns = [
    path("announcement/", AnnouncementAPI.as_view(), name="announcement_api"),
    path("announcement_detail/", AnnouncementDetailAPI.as_view(), name="announcement_detail_api"),
]
