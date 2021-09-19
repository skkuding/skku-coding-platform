from django.urls import path

from ..views.student import AssignmentAPI

urlpatterns = [
    path("course/assignment/", AssignmentAPI.as_view(), name="assignment_api"),
]
