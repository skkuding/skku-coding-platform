from django.urls import path

from ..views.professor import AssignmentProblemAPI, AddAssignmentProblemAPI, CourseProblemAPI, AddCourseProblemAPI

urlpatterns = [
    path("course/assignment/problem/", AssignmentProblemAPI.as_view(), name="assignment_problem_professor_api"),
    path("course/assignment/add_problem_from_public/", AddAssignmentProblemAPI.as_view(), name="add_assignment_problem_from_public_api"),
    path("course/problem/", CourseProblemAPI.as_view(), name="course_problem_professor_api"),
    path("course/add_problem_from_public/", AddCourseProblemAPI.as_view(), name="add_course_problem_from_public_api"),
]
