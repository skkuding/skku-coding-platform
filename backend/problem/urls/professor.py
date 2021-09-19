from django.urls import path

from ..views.professor import AssignmentProblemAPI, AddAssignmentProblemAPI

urlpatterns = [
    path("course/assignment/problem/", AssignmentProblemAPI.as_view(), name="assignment_problem_professor_api"),
    path("course/assignment/add_problem_from_public/", AddAssignmentProblemAPI.as_view(), name="add_assignment_problem_from_public_api"),
]
