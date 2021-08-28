from django.conf.urls import url

from ..views.professor import AssignmentAPI, DownloadAssignmentSubmissions

urlpatterns = [
    url(r"^course/assignment/?$", AssignmentAPI.as_view(), name="assignment_professor_api"),
    url(r"^download_submissions/?$", DownloadAssignmentSubmissions.as_view(), name="download_assignment_submissions"),
]
