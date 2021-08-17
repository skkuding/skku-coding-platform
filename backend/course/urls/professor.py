from django.conf.urls import url

from ..views.professor import CourseAPI, StudentManagementAPI

urlpatterns = [
    url(r"^course/?$", CourseAPI.as_view(), name="course_professor_api"),
    url(r"^course/students/?$", StudentManagementAPI.as_view(), name="student_management_api")
]
