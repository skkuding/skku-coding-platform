from django.urls import path

from ..views import SMTPAPI, JudgeServerAPI, WebsiteConfigAPI, TestCasePruneAPI, SMTPTestAPI
from ..views import ReleaseNotesAPI, DashboardInfoAPI

urlpatterns = [
    path("smtp/", SMTPAPI.as_view(), name="smtp_admin_api"),
    path("smtp_test/", SMTPTestAPI.as_view(), name="smtp_test_api"),
    path("website/", WebsiteConfigAPI.as_view(), name="website_config_api"),
    path("judge_server/", JudgeServerAPI.as_view(), name="judge_server_api"),
    path("prune_test_case/", TestCasePruneAPI.as_view(), name="prune_test_case_api"),
    path("versions/", ReleaseNotesAPI.as_view(), name="get_release_notes_api"),
    path("dashboard_info/", DashboardInfoAPI.as_view(), name="dashboard_info_api"),
]
