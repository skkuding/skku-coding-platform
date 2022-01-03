from django.urls import path

from ..views.oj import BannerAPI

urlpatterns = [
    path("banner/", BannerAPI.as_view(), name="banner_api")
]
