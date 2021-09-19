from django.urls import path

from ..views.student import CourseAPI

urlpatterns = [
    path("course/", CourseAPI.as_view(), name="course_api"),
]
