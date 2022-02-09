from django.urls import path

from .views import ProfileSubmissionListAPI, SubmissionAPI, SubmissionListAPI, ContestSubmissionListAPI, SubmissionExistsAPI

urlpatterns = [
    path("submission/", SubmissionAPI.as_view(), name="submission_api"),
    path("submissions/", SubmissionListAPI.as_view(), name="submission_list_api"),
    path("submission_exists/", SubmissionExistsAPI.as_view(), name="submission_exists"),
    path("contest_submissions/", ContestSubmissionListAPI.as_view(), name="contest_submission_list_api"),
    path("profile_submissions/", ProfileSubmissionListAPI.as_view(), name="profile_submission_list_api"),
]
