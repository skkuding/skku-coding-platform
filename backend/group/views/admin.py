from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.decorators import super_admin_required

# from group.models import Group, GroupMemberJoin
from group.serializers import GroupRegistrationRequestSerializer, GroupDetailSerializer, CreateGroupSerializer, GroupSummarySerializer, GroupMemberSerializer, \
                                GroupMemberJoinSerializer
from utils.api import APIView, validate_serializer

from ..models import GroupRegistrationRequest, Group, GroupMember, GroupMemberJoin


class AdminGroupRegistrationRequestAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[],
        operation_description="Request to group registration",
        responses={200: GroupRegistrationRequestSerializer(many=True)}
    )
    @super_admin_required
    def get(self, request):
        group_registration_requests = GroupRegistrationRequest.objects.all()
        return self.success(GroupRegistrationRequestSerializer(group_registration_requests, many=True).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="request_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a registration request.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                name="accept",
                in_=openapi.IN_QUERY,
                description="if accept, accept registration request and create group. else, just delete registration request",
                type=openapi.TYPE_BOOLEAN,
                required=True
            )
        ],
        operation_description="if accept is true, accept registration request and create group.\
                                else, just delete registration request. \
                                Be careful if accept is not given, also considered as accepted=False",
        responses={200: GroupDetailSerializer}
    )
    @super_admin_required
    def delete(self, request):
        request_id = request.GET.get("request_id")
        accept = request.GET.get("accept")

        if not accept:
            try:
                GroupRegistrationRequest.objects.get(id=request_id).delete()
                return self.success("Successfully deleted group registration request")
            except GroupRegistrationRequest.DoesNotExist:
                return self.error("Invalid group registration request id")

        try:
            group_registration_request = GroupRegistrationRequest.objects.get(id=request_id)
        except GroupRegistrationRequest.DoesNotExist:
            return self.error("Invalid group registration request id")
        creator = group_registration_request.created_by
        group = Group.objects.create(
            name=group_registration_request.name,
            short_description=group_registration_request.short_description,
            description=group_registration_request.description,
            is_official=group_registration_request.is_official,

            created_by=creator
        )
        group.members.add(creator, through_defaults={"is_group_admin": True})
        GroupRegistrationRequest.objects.get(id=request_id).delete()

        return self.success(GroupDetailSerializer(group).data)


class GroupAdminAPI(APIView):
    @swagger_auto_schema(
        request_body=CreateGroupSerializer,
        operation_description="Request to register a group",
        responses={200: CreateGroupSerializer}
    )
    @validate_serializer(CreateGroupSerializer)
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return self.error("Login First")

        data = request.data
        name = data["name"]

        if GroupRegistrationRequest.objects.filter(name=name).exists() or Group.objects.filter(name=name).exists():
            return self.error("Duplicate group name")

        group = Group.objects.create(
            name=name,
            short_description=data["short_description"],
            description=data["description"],
            is_official=data["is_official"],
            created_by=request.user
        )
        group.members.add(user, through_defaults={"is_group_admin": True})
        return self.success(GroupDetailSerializer(group).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a group. if id is not given, return group list, else return detail of a group",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        operation_description="Get group list or detail of a group"
    )
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return self.error("Login First")

        group_id = request.GET.get("id")

        # Group List
        if not group_id:
            groups = Group.objects.all()
            return self.success(GroupSummarySerializer(groups, many=True).data)

        # Group Detail
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return self.error("Group does not exist")
        data = GroupDetailSerializer(group).data

        data["members"] = GroupMemberSerializer(GroupMember.objects.filter(group=group_id), many=True).data

        if GroupMember.objects.filter(is_group_admin=True, group=group, user=user).exists():
            group_member_join = GroupMemberJoin.objects.filter(group=group)
            data["group_member_join"] = GroupMemberJoinSerializer(group_member_join, many=True).data

        return self.success(data)
