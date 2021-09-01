from django.conf.urls import include, url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="SKKU Coding Platform",
        default_version="v1",
        description="QingdaoU OJ 기반 Online Judge 시스템",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    url(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    url(r"^api/", include("account.urls.oj")),
    url(r"^api/admin/", include("account.urls.admin")),
    url(r"^api/", include("announcement.urls.oj")),
    url(r"^api/admin/", include("announcement.urls.admin")),
    url(r"^api/", include("conf.urls.oj")),
    url(r"^api/admin/", include("conf.urls.admin")),
    url(r"^api/professor/", include("conf.urls.professor")),
    url(r"^api/", include("problem.urls.oj")),
    url(r"^api/admin/", include("problem.urls.admin")),
    url(r"^api/lecture/", include("problem.urls.student")),
    url(r"^api/lecture/professor/", include("problem.urls.professor")),
    url(r"^api/", include("contest.urls.oj")),
    url(r"^api/admin/", include("contest.urls.admin")),
    url(r"^api/", include("submission.urls")),
    url(r"^api/admin/", include("utils.urls")),
    url(r"^api/lecture/", include("course.urls.student")),
    url(r"^api/lecture/professor/", include("course.urls.professor")),
    url(r"^api/lecture/", include("assignment.urls.student")),
    url(r"^api/lecture/professor/", include("assignment.urls.professor")),
]
