from django.conf.urls import url

from ..views.professor import AssignmentProblemAPI, AddAssignmentProblemAPI
from ..views.admin import CompileSPJAPI, TestCaseTextAPI

urlpatterns = [
    url(r"^compile_spj/?$", CompileSPJAPI.as_view(), name="assignment_compile_spj"),
    url(r"^course/assignment/problem/?$", AssignmentProblemAPI.as_view(), name="assignment_problem_professor_api"),
    url(r"^course/assignment/add_problem_from_public/?$", AddAssignmentProblemAPI.as_view(), name="add_assignment_problem_from_public_api"),
    url(r"^testcase_text/?$", TestCaseTextAPI.as_view(), name="assignment_testcase_text_api")
]
