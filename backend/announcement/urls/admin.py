from django.urls import path

from ..views.admin import AnnouncementAdminAPI

urlpatterns = [
    path("announcement/", AnnouncementAdminAPI.as_view(), name="announcement_admin_api"),
]
