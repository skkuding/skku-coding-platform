from django.urls import path
from ..views.oj import GroupRegistrationRequestAPI, GroupAPI, GroupDetailAPI


urlpatterns = [
    path("group/register_request", GroupRegistrationRequestAPI.as_view(), name="group_register_request_api"),
    path("group/", GroupAPI.as_view(), name="group_api"),
    path("group/detail", GroupDetailAPI.as_view(), name="group_detail_api")
]
