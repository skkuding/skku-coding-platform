from django.conf.urls import url

from .views import (SubmissionAPI, SubmissionListAPI, ContestSubmissionListAPI, AssignmentSubmissionListAPI,
                    AssignmentSubmissionListProfessorAPI, SubmissionExistsAPI, EditSubmissionScoreAPI)

urlpatterns = [
    url(r"^submission/?$", SubmissionAPI.as_view(), name="submission_api"),
    url(r"^submissions/?$", SubmissionListAPI.as_view(), name="submission_list_api"),
    url(r"^submission_exists/?$", SubmissionExistsAPI.as_view(), name="submission_exists"),
    url(r"^contest_submissions/?$", ContestSubmissionListAPI.as_view(), name="contest_submission_list_api"),
    url(r"^assignment_submissions/?$", AssignmentSubmissionListAPI.as_view(), name="assignment_submission_list_api"),
    url(r"^assignment_submissions_professor/?$", AssignmentSubmissionListProfessorAPI.as_view(), name="assignment_submission_list_professor_api"),
    url(r"^edit_submission_score/?$", EditSubmissionScoreAPI.as_view(), name="edit_submission_score_api"),
]
