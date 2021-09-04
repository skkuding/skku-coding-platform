from django.conf.urls import url

from ..views.professor import AssignmentProblemAPI, AddAssignmentProblemAPI

urlpatterns = [
    url(r"^course/assignment/problem/?$", AssignmentProblemAPI.as_view(), name="assignment_problem_professor_api"),
    url(r"^course/assignment/add_problem_from_public/?$", AddAssignmentProblemAPI.as_view(), name="add_assignment_problem_from_public_api"),
]
