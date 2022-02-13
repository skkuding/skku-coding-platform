from django.urls import path
from ..views.admin import AdminGroupRegistrationRequestAPI, GroupAdminAPI


urlpatterns = [
    path("group/registration_request/", AdminGroupRegistrationRequestAPI.as_view(), name="group_registration_request_admin_api"),
    path("group/", GroupAdminAPI.as_view(), name="group_admin_api")
]
