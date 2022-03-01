from django.urls import path

from ..views.student import QuestionAPI, AnswerAPI

urlpatterns = [
    path("course/question/", QuestionAPI.as_view(), name="question_api"),
    path("course/question/answer/", AnswerAPI.as_view(), name="answer_api")
]
