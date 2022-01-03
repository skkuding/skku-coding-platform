from django.urls import path

from ..views.admin import BannerAdminAPI

urlpatterns = [
    path("banner/", BannerAdminAPI.as_view(), name="banner_admin_api")
]
