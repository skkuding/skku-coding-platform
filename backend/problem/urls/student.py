from django.urls import path

from ..views.student import AssignmentProblemAPI

urlpatterns = [
    path("course/assignment/problem/", AssignmentProblemAPI.as_view(), name="assignment_problem_student_api"),
]
