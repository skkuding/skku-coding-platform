from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# from group.models import UserGroup, GroupApplication
from group.serializers import GroupSummarySerializer, CreateGroupRegistrationRequestSerializer, GroupRegistrationRequestSerializer
from utils.api import APIView, validate_serializer

from account.models import User
from ..models import GroupRegistrationRequest


class GroupRegistrationRequestAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Request to register a group"
    )
    @validate_serializer(CreateGroupRegistrationRequestSerializer)
    def post(self, request):
        data = request.data
        group = GroupRegistrationRequest.objects.create(
            name=data["name"],
            short_description=data["short_description"],
            description=data["description"],
            is_official=data["is_official"]
        )
        return self.success(GroupRegistrationRequestSerializer(group).data)


class GroupAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Get group list"
    )
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            # Why self.success ?
            return self.success()
        username = request.GET.get("username")
        try:
            if username:
                if not username == user.username:
                    return self.error("You only can get your profile")
                user = User.objects.get(username=username, is_disabled=False)
            else:
                return self.error("Username parameter is necessary")
                # The api returns your own information, you can return real_name
        except User.DoesNotExist:
            return self.error("User does not exist")
        admin_groups = user.admin_groups.all()
        groups = user.groups.all()

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
        pass

    # for admin_group in admin_groups:
    #     try:
    #         data["admin_groups"]["application"] = GroupApplication.objects.get(user_group = admin_group)
    #     except GroupApplication.DoesNotExist:
    #         return self.error("Group Application does not exist")
