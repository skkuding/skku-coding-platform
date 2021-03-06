from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer
from utils.api import APIView
from utils.shortcuts import check_is_id


class AnnouncementAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Get Announcement"
    )
    def get(self, request):
        announcements = Announcement.objects.filter(visible=True)
        return self.success(self.paginate_data(request, announcements, AnnouncementSerializer))


class AnnouncementDetailAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of an announcement",
                required=True,
                type=openapi.TYPE_INTEGER,
            )
        ],
        operation_description="Get detail of single annoucement"
    )
    def get(self, request):
        id = request.GET.get("id")
        if not id or not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            announcement = Announcement.objects.get(id=id, visible=True)
        except Announcement.DoesNotExist:
            return self.error("Announcement does not exist")
        data = {}
        data["current"] = AnnouncementSerializer(announcement).data
        prev_announcements = Announcement.objects.filter(id__lt=id, visible=True)
        if prev_announcements:
            data["previous"] = AnnouncementSerializer(prev_announcements.latest("create_time")).data
        next_announcements = Announcement.objects.filter(id__gt=id, visible=True)
        if next_announcements:
            data["next"] = AnnouncementSerializer(next_announcements.earliest("create_time")).data
        return self.success(data)
