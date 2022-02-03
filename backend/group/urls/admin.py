from django.urls import path
from ..views.admin import AdminGroupRegistrationRequestAPI


urlpatterns = [
    path("group/registration_request/", AdminGroupRegistrationRequestAPI.as_view(), name="group_registration_request_admin_api")
]
