from django.urls import path

from ..views.student import BookmarkCourseAPI, CourseAPI

urlpatterns = [
    path("course/", CourseAPI.as_view(), name="course_api"),
    path("bookmark_course/", BookmarkCourseAPI.as_view(), name="bookmark_course_api"),
]
