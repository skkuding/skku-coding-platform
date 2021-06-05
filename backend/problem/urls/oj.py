from django.urls import path

from ..views.oj import ProblemTagAPI, ProblemAPI, ContestProblemAPI, PickOneAPI

urlpatterns = [
    path("problem/tags/", ProblemTagAPI.as_view(), name="problem_tag_list_api"),
    path("problem/", ProblemAPI.as_view(), name="problem_api"),
    path("pickone/", PickOneAPI.as_view(), name="pick_one_api"),
    path("contest/problem/", ContestProblemAPI.as_view(), name="contest_problem_api"),
]
