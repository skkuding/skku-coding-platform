from django.urls import path

from .views import (SubmissionAPI, SubmissionListAPI, ContestSubmissionListAPI, AssignmentSubmissionListAPI,
                    AssignmentSubmissionListProfessorAPI, SubmissionExistsAPI, EditSubmissionScoreAPI)
from .views import ProfileSubmissionListAPI, SubmissionAPI, SubmissionListAPI, ContestSubmissionListAPI, SubmissionExistsAPI

urlpatterns = [
    path("submission/", SubmissionAPI.as_view(), name="submission_api"),
    path("submissions/", SubmissionListAPI.as_view(), name="submission_list_api"),
    path("submission_exists/", SubmissionExistsAPI.as_view(), name="submission_exists"),
    path("contest_submissions/", ContestSubmissionListAPI.as_view(), name="contest_submission_list_api"),
    path("assignment_submissions/", AssignmentSubmissionListAPI.as_view(), name="assignment_submission_list_api"),
    path("assignment_submissions_professor/", AssignmentSubmissionListProfessorAPI.as_view(), name="assignment_submission_list_professor_api"),
    path("edit_submission_score/", EditSubmissionScoreAPI.as_view(), name="edit_submission_score_api"),
    path("profile_submissions/", ProfileSubmissionListAPI.as_view(), name="profile_submission_list_api"),
]
