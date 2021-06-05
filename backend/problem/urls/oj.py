from django.urls import path

from ..views.oj import ProblemTagAPI, ProblemAPI, ContestProblemAPI

urlpatterns = [
    path("problem/tags/", ProblemTagAPI.as_view(), name="problem_tag_list_api"),
    path("problem/", ProblemAPI.as_view(), name="problem_api"),
    path("contest/problem/", ContestProblemAPI.as_view(), name="contest_problem_api"),
]
