from django.urls import path

from ..views.professor import *

urlpatterns = [
    path("course/question", QuestionAPI.as_view(), name="question_professor_api"),
]