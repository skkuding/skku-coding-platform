from django.urls import path

from ..views.professor import BookmarkCourseAPI, CourseAPI, StudentManagementAPI

urlpatterns = [
    path("course/", CourseAPI.as_view(), name="course_professor_api"),
    path("course/students/", StudentManagementAPI.as_view(), name="student_management_api"),
    path("bookmark_course/", BookmarkCourseAPI.as_view(), name="bookmark_professor_api")
]
