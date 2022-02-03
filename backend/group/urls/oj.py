from django.urls import path
from ..views.oj import GroupMemberJoinAPI, GroupMemberAPI, GroupRegistrationRequestAPI, GroupAPI


urlpatterns = [
    path("group/registration_request/", GroupRegistrationRequestAPI.as_view(), name="group_registration_request_api"),
    path("group/", GroupAPI.as_view(), name="group_api"),
    path("group/member_join/", GroupMemberJoinAPI.as_view(), name="group_member_join_api"),
    path("group/member/", GroupMemberAPI.as_view(), name="group_member_api")
]
