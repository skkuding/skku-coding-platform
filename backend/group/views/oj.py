from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from group.serializers import CreateGroupApplicationSerializer, EditGroupMemberPermissionSerializer, GroupApplicationSerializer, GroupDetailSerializer
from group.serializers import GroupRegistrationRequestSerializer, GroupSummarySerializer, CreateGroupRegistrationRequestSerializer
from utils.api import APIView, validate_serializer
from utils.decorators import check_group_admin

from account.models import User
from django.db.models import Q
from ..models import GroupApplication, GroupRegistrationRequest, Group


class GroupRegistrationRequestAPI(APIView):
    @swagger_auto_schema(
        request_body=CreateGroupApplicationSerializer,
        operation_description="Request to register a group",
        responses={200: GroupRegistrationRequestSerializer}
    )
    @validate_serializer(CreateGroupRegistrationRequestSerializer)
    def post(self, request):
        data = request.data
        name = data["name"]

        if GroupRegistrationRequest.objects.filter(name=name).exists() or Group.objects.filter(name=name).exists():
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
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a group. if id is not given, return group list, else return detail of a group",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        operation_description="Get group list"
    )
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return self.error("Login First")

        group_id = request.GET.get("id")

        # Group List
        if not group_id:
            groups_not_admin = Group.objects.filter(groupmember__is_admin=False, groupmember__user=user)
            print(groups_not_admin)
            groups_admin = Group.objects.filter(groupmember__is_admin=True, groupmember__user=user)
            other_groups = Group.objects.exclude(Q(members=user))

            data = {}
            data["admin_groups"] = GroupSummarySerializer(groups_not_admin, many=True).data
            data["groups"] = GroupSummarySerializer(groups_admin, many=True).data
            data["other_groups"] = GroupSummarySerializer(other_groups, many=True).data

            return self.success(data)

        # Group Detail
        else:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return self.error("Group does not exist")
            data = GroupDetailSerializer(group).data

            if Group.objects.filter(admin_members=user).exists():
                try:
                    group_application = GroupApplication.objects.filter(group=group)
                except GroupApplication.DoesNotExist:
                    self.error("Group Application model does not exist")
                data["group_application"] = GroupApplicationSerializer(group_application, many=True).data

            return self.success(data)


class GroupMemberAPI(APIView):
    # Change User Group Permission
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="member_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of member id",
                required=True
            ),
            openapi.Parameter(
                name="is_admin", in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Set permission of selected member.",
                required=True
            ),
            openapi.Parameter(
                name="group_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Unique id of group id",
                required=True
            )
        ],
        operation_description="Change group member permission"
    )
    @validate_serializer(EditGroupMemberPermissionSerializer)
    @check_group_admin()
    def put(self, request):
        data = request.data
        user = request.user

        try:
            group = Group.objects.get(id=data["group_id"])
        except Group.DoesNotExist:
            return self.error("Group does not exist")

        if data["is_admin"]:
            try:
                member = group.members.get(id=data["member_id"])
            except User.DoesNotExist:
                return self.error("Member does not exists")
            group.admin_members.add(member)
            group.members.remove(member)
            return self.success(GroupDetailSerializer(group).data)

        else:
            if not (group.created_by.id == user.id):
                return self.error("Only group creator can change group admin's permission")
            else:
                try:
                    admin_member = group.admin_members.get(id=data["member_id"])
                except User.DoesNotExist:
                    return self.error("Member Does not exists")
                group.members.add(admin_member)
                group.admin_members.remove(admin_member)
                return self.success(GroupDetailSerializer(group).data)


class GroupApplicationAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="group_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of group.",
                required=True
            ),
            openapi.Parameter(
                name="description", in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Group Application Description explaining who the user is",
                required=True
            )
        ],
        operation_description="Post a group application"
    )
    @validate_serializer(CreateGroupApplicationSerializer)
    def post(self, request):
        user = request.user
        group_id = request.data["group_id"]
        description = request.data["description"]

        group_application = GroupApplication.objects.create(
            group_id=group_id,
            description=description,
            created_by=user
        )

        return self.success(GroupApplicationSerializer(group_application).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="group_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of group.",
                required=True
            ),
            openapi.Parameter(
                name="application_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of application",
                required=True
            ),
            openapi.Parameter(
                name="accept", in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="true if accept else reject the application",
                required=True
            ),
        ],
        operation_description="Resolve group application"
    )
    @check_group_admin()
    def delete(self, request):
        group_id = request.GET.get("group_id")
        application_id = request.GET.get("application_id")
        accept = request.GET.get("accept")

        try:
            group_application = GroupApplication.objects.get(id=application_id)
        except GroupApplication.DoesNotExist:
            self.error("Group application does not exist")

        if not accept:
            group_application.delete()
            return self.success("Successfully rejected a group application")

        group_application_created_by = group_application.created_by
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            self.error("Group does not exist")

        if group.members.filter(id=group_application_created_by.id).exists() or group.admin_members.filter(id=group_application_created_by.id).exists():
            self.error("Already in group")

        group.members.add(group_application_created_by)
        group_application.delete()

        return self.success(GroupDetailSerializer(group).data)
