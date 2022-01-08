from django.urls import path

from ..views import AnswerAPI

urlpatterns = [
    path("course/question/answer", AnswerAPI.as_view(), name="answer_api")
]