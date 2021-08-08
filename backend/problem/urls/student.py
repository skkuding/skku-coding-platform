from django.conf.urls import url

from ..views.student import AssignmentProblemAPI

urlpatterns = [
    url(r"^course/assignment/problem/?$", AssignmentProblemAPI.as_view(), name="assignment_problem_student_api"),
]
