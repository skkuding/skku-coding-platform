from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.decorators import super_admin_required

# from group.models import Group, GroupApplication
from group.serializers import GroupRegistrationRequestSerializer, GroupDetailSerializer
from utils.api import APIView

from ..models import GroupRegistrationRequest, Group


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
                required=False
            ),
            openapi.Parameter(
                name="accept",
                in_=openapi.IN_QUERY,
                description="if accept, accept registration request and create group. else, just delete registration request",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        operation_description="Request to group registration",
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
        group.members.add(creator, through_defaults={"is_admin": True})
        GroupRegistrationRequest.objects.get(id=request_id).delete()

        return self.success(GroupDetailSerializer(group).data)
