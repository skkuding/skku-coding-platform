from utils.api import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer


class AnnouncementAPI(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="visible",
                type=bool,
            )
        ],
        description='Get Announcement'
    )
    def get(self, request):
        announcements = Announcement.objects.filter(visible=True)
        return self.success(self.paginate_data(request, announcements, AnnouncementSerializer))
