from django.urls import path

from ..views.admin import ContestAnnouncementAPI, ContestAPI, ContestRankAPI, DownloadContestSubmissions

urlpatterns = [
    path("contest/", ContestAPI.as_view(), name="contest_admin_api"),
    path("contest/announcement/", ContestAnnouncementAPI.as_view(), name="contest_announcement_admin_api"),
    path("download_submissions/", DownloadContestSubmissions.as_view(), name="acm_contest_helper"),
    path("contest/rank/", ContestRankAPI.as_view(), name="contest_rank_api")
]
