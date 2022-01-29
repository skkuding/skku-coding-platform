from drf_yasg.utils import swagger_auto_schema
from utils.decorators import super_admin_required

# from group.models import UserGroup, GroupApplication
from group.serializers import CreateGroupSerializer, GroupRegistrationRequestSerializer, GroupDetailSerializer
from utils.api import APIView, validate_serializer, CSRFExemptAPIView

from ..models import GroupRegistrationRequest, UserGroup


class AdminGroupRegistrationRequestAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Response to group registration",
        responses={200: GroupRegistrationRequestSerializer(many=True)}
    )
    @super_admin_required
    def get(self, request):
        group_registration_requests = GroupRegistrationRequest.objects.all()
        return self.success(GroupRegistrationRequestSerializer(group_registration_requests, many=True))


class AdminGroupRegistrationResponseAPI(CSRFExemptAPIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Response to group registration",
        responses={200: GroupRegistrationRequestSerializer}
    )
    @validate_serializer(CreateGroupSerializer)
    @super_admin_required
    def post(self, request):
        data = request.data

        if (not data["accept"]):
            try:
                GroupRegistrationRequest.objects.delete(id=data["request_id"])
                return self.success("Successfully deleted group registration request")
            except GroupRegistrationRequest.DoesNotExist:
                return self.error("Invalid group registration request id")

        try:
            group_registration_request = GroupRegistrationRequest.objects.get(id=data["request+id"])
        except GroupRegistrationRequest.DoesNotExist:
            return self.error("Invalid group registration request id")
        group = UserGroup.objects.create(
            name=group_registration_request["name"],
            short_description=group_registration_request["short_description"],
            description=group_registration_request["description"],
            is_official=group_registration_request["is_official"]
        )
        GroupRegistrationRequest.objects.delete(id=data["request_id"])

        return self.success(GroupDetailSerializer(group).data)
