from django.urls import path
from ..views.admin import AdminGroupRegistrationRequestAPI, AdminGroupRegistrationResponseAPI


urlpatterns = [
    path("admin/group/register_request", AdminGroupRegistrationRequestAPI.as_view(), name="admin_group_register_request_api"),
    path("admin/group/register_response", AdminGroupRegistrationResponseAPI.as_view(), name="admin_group_register_response_api")
]
