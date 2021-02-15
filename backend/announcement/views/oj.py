from utils.api import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AnnouncementAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Get Announcement"
    )
    def get(self, request):
        announcements = Announcement.objects.filter(visible=True)
        return self.success(self.paginate_data(request, announcements, AnnouncementSerializer))
