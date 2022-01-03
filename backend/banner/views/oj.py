from drf_yasg.utils import swagger_auto_schema

from banner.models import Banner
from banner.serializers import BannerSerializer
from utils.api import APIView


class BannerAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Get Banner Image List"
    )
    def get(self, request):
        banners = Banner.objects.filter(visible=True)
        data = {}
        data["path"] = BannerSerializer(banners, many=True).data
        return self.success(data)
