from django.urls import path

from ..views.admin import SubmissionRejudgeAPI

urlpatterns = [
    path("submission/rejudge", SubmissionRejudgeAPI.as_view(), name="submission_rejudge_api"),
]
