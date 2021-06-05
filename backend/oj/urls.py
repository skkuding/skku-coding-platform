from django.urls import include, path


urlpatterns = [
    path("api/", include("account.urls.oj")),
    path("api/admin/", include("account.urls.admin")),
    path("api/", include("announcement.urls.oj")),
    path("api/admin/", include("announcement.urls.admin")),
    path("api/", include("conf.urls.oj")),
    path("api/admin/", include("conf.urls.admin")),
    path("api/", include("problem.urls.oj")),
    path("api/admin/", include("problem.urls.admin")),
    path("api/", include("contest.urls.oj")),
    path("api/admin/", include("contest.urls.admin")),
    path("api/", include("submission.urls.oj")),
    path("api/admin/", include("submission.urls.admin")),
    path("api/admin/", include("utils.urls")),
]
