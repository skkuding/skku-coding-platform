from django.urls import path

from ..views import ProfessorDashboardInfoAPI

urlpatterns = [
    path("professor_dashboard_info/", ProfessorDashboardInfoAPI.as_view(), name="professor_dashboard_info_api"),
]
