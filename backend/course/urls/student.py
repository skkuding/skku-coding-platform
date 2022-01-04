from django.conf.urls import url

from ..views.student import CourseAPI, QuestionAPI

urlpatterns = [
    url(r"^course/?$", CourseAPI.as_view(), name="course_api"),
    url(r"^question/?$", QuestionAPI.as_view(), name="question_api"),
]
