from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from group.serializers import CreateGroupApplicationSerializer, EditGroupMemberPermissionSerializer, GroupApplicationSerializer, GroupDetailSerializer, GroupMemberSerializer
from group.serializers import GroupRegistrationRequestSerializer, GroupSummarySerializer, CreateGroupRegistrationRequestSerializer
from utils.api import APIView, validate_serializer
from utils.decorators import check_group_admin

from django.db.models import Q
from ..models import GroupApplication, GroupMember, GroupRegistrationRequest, Group


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

            if GroupMember.objects.filter(is_admin=True, group=group, user=user).exists():
                group_application = GroupApplication.objects.filter(group=group)
                data["group_application"] = GroupApplicationSerializer(group_application, many=True).data

            return self.success(data)


class GroupMemberAPI(APIView):
    # Change User Group Permission
    @swagger_auto_schema(
        request_body=EditGroupMemberPermissionSerializer,
        operation_description="Change group member permission",
        responses={200: GroupMemberSerializer}
    )
    @validate_serializer(EditGroupMemberPermissionSerializer)
    @check_group_admin()
    def put(self, request):
        data = request.data
        user = request.user

        if data["is_admin"]:
            try:
                member = GroupMember.objects.get(user=data["user_id"], group=data["group_id"])
            except GroupMember.DoesNotExist:
                return self.error("Group Member does not exists")
            member.is_admin = data["is_admin"]  # True
            member.save()
            return self.success(GroupMemberSerializer(member).data)

        else:
            # Only group creator can downgrade group admin's permission.
            try:
                group = Group.objects.get(id=data["group_id"])
            except Group.DoesNotExist:
                return self.error("Group does not exists")
            if not (group.created_by.id == user.id):
                return self.error("Only group creator can change group admin's permission")

            try:
                member = GroupMember.objects.get(user=data["user_id"], group=data["group_id"])
            except GroupMember.DoesNotExist:
                return self.error("Group member does not exist")
            member.is_admin = data["is_admin"]  # False
            member.save()
            return self.success(GroupMemberSerializer(member).data)


class GroupApplicationAPI(APIView):
    @swagger_auto_schema(
        request_body=CreateGroupApplicationSerializer,
        operation_description="Post a group application",
        responses={200: GroupApplicationSerializer}
    )
    @validate_serializer(CreateGroupApplicationSerializer)
    def post(self, request):
        user = request.user
        group_id = request.data["group_id"]
        description = request.data["description"]

        if Group.objects.filter(id=group_id, members=user).exists():
            return self.error("You are already a member of this group.")

        if GroupApplication.objects.filter(group=group_id, created_by=user).exists():
            return self.error("You have already submitted your application to this group.")

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

        if group.members.filter(id=group_application_created_by.id).exists():
            self.error("This user is already a member. This application may be already resolved.")

        group.members.add(group_application_created_by)
        group_application.delete()

        return self.success(GroupDetailSerializer(group).data)
