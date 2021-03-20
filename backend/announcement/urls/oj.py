from django.conf.urls import url

from ..views.oj import AnnouncementAPI, AnnouncementDetailAPI

urlpatterns = [
    url(r"^announcement/?$", AnnouncementAPI.as_view(), name="announcement_api"),
    url(r"^announcement_detail/?$", AnnouncementDetailAPI.as_view(), name="announcement_detail_api"),
]
