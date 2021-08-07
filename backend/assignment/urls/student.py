from django.conf.urls import url

from ..views.student import AssignmentAPI

urlpatterns = [
    url(r"^course/assignment/?$", AssignmentAPI.as_view(), name="assignment_api"),
]