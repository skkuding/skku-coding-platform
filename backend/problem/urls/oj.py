from django.urls import path

from ..views.oj import ProblemTagAPI, ProblemAPI, ContestProblemAPI, BankProblemAPI, ProblemSetGroupAPI, ProblemSetAPI

urlpatterns = [
    path("problem/tags/", ProblemTagAPI.as_view(), name="problem_tag_list_api"),
    path("problem/", ProblemAPI.as_view(), name="problem_api"),
    path("contest/problem/", ContestProblemAPI.as_view(), name="contest_problem_api"),
    path("bank/problem/", BankProblemAPI.as_view(), name="bank_problem_api"),
    path("problemset/group/", ProblemSetGroupAPI.as_view(), name="problem_set_group_api"),
    path("problemset/", ProblemSetAPI.as_view(), name="problem_set_api"),
]
