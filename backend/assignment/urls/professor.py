from django.conf.urls import url

from ..views.professor import AssignmentAPI

urlpatterns = [
    url(r"^course/assignment/?$", AssignmentAPI.as_view(), name="assignment_professor_api"),
]