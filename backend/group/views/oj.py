from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# from group.models import UserGroup, GroupApplication
from group.serializers import GroupDetailSerializer, GroupSummarySerializer, CreateGroupRegistrationRequestSerializer, GroupRegistrationRequestSerializer
from utils.api import APIView, validate_serializer, CSRFExemptAPIView

from account.models import User
from ..models import GroupRegistrationRequest, UserGroup


class GroupRegistrationRequestAPI(CSRFExemptAPIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Request to register a group"
    )
    @validate_serializer(CreateGroupRegistrationRequestSerializer)
    def post(self, request):
        data = request.data
        name = data["name"]

        if GroupRegistrationRequest.objects.filter(name=name).exists() or UserGroup.objects.filter(name=name).exists():
            return self.error("Duplicate group name")

        registration_request = GroupRegistrationRequest.objects.create(
            name=name,
            short_description=data["short_description"],
            description=data["description"],
            is_official=data["is_official"],
            created_by=request.user
        )
        return self.success(GroupRegistrationRequestSerializer(registration_request).data)


class GroupAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Get group list"
    )
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return self.error("Login First")
        username = request.GET.get("username")
        try:
            if username:
                if not username == user.username:
                    return self.error("You only can get your group")
                user = User.objects.get(username=username, is_disabled=False)
            else:
                return self.error("Username parameter is necessary")
        except User.DoesNotExist:
            return self.error("User does not exist")
        admin_groups = user.admin_groups.all()
        groups = user.groups.all()
        # all_groups = UserGroup.objects.filter(admin_members__admin_groups="")

        data = {}
        data["admin_groups"] = GroupSummarySerializer(admin_groups, many=True).data
        data["groups"] = GroupSummarySerializer(groups, many=True)

        return self.success(data)


class GroupDetailAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of group.",
                required=True
            ),
        ],
        operation_description="Get group details"
    )
    def get(self, request):
        group_id = request.GET.get("group_id")
        if not group_id:
            return self.error("Group id parameter is necessary")
        try:
            group = UserGroup.objects.get(id=group_id)
        except UserGroup.DoesNotExist:
            return self.error("Group does not exist")
        return self.success(GroupDetailSerializer(group).data)

