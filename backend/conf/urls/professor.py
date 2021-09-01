from django.conf.urls import url

from ..views import ProfessorDashboardInfoAPI

urlpatterns = [
    url(r"^professor_dashboard_info", ProfessorDashboardInfoAPI.as_view(), name="professor_dashboard_info_api"),
]
