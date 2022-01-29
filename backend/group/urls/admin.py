from django.urls import path
from ..views.admin import AdminGroupRegistrationRequestAPI, AdminGroupRegistrationResponseAPI


urlpatterns = [
    path("group/registration_request", AdminGroupRegistrationRequestAPI.as_view(), name="group_registration_request_admin_api"),
    path("group/registration_response", AdminGroupRegistrationResponseAPI.as_view(), name="group_registration_response_admin_api")
]
