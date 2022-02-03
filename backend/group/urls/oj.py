from django.urls import path
from ..views.oj import GroupApplicationAPI, GroupMemberAPI, GroupRegistrationRequestAPI, GroupAPI


urlpatterns = [
    path("group/registration_request/", GroupRegistrationRequestAPI.as_view(), name="group_registration_request_api"),
    path("group/", GroupAPI.as_view(), name="group_api"),
    path("group/application/", GroupApplicationAPI.as_view(), name="group_application_api"),
    path("group/member/", GroupMemberAPI.as_view(), name="group_member_api")
]
