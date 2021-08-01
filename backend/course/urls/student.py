from django.conf.urls import url
from django.urls.resolvers import URLPattern

from ..views.student import CourseAPI

urlpatterns = [
    url(r"^course/?$", CourseAPI.as_view(), name="course_api"),
]