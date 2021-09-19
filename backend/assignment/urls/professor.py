from django.urls import path

from ..views.professor import AssignmentAPI, DownloadAssignmentSubmissions

urlpatterns = [
    path("course/assignment/", AssignmentAPI.as_view(), name="assignment_professor_api"),
    path("download_submissions/", DownloadAssignmentSubmissions.as_view(), name="download_assignment_submissions"),
]
