from django.urls import path

from ..views.admin import UserAdminAPI, GenerateUserAPI

urlpatterns = [
    path("user/", UserAdminAPI.as_view(), name="user_admin_api"),
    path("generate_user/", GenerateUserAPI.as_view(), name="generate_user_api"),
]
