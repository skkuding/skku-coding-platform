from .models import GroupRegistrationRequest, UserGroup
from utils.api import serializers


class CreateGroupRegistrationRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    is_official = serializers.BooleanField()
    # logo = serializers.ImageField()


class GroupRegistrationRequestSerializer(serializers.Serializer):
    class Meta:
        model = GroupRegistrationRequest
        field = "__all__"


class CreateGroupSerializer(serializers.Serializer):
    accept = serializers.BooleanField()
    request_id = serializers.IntegerField()
    # logo = serializers.ImageField()


class GroupSummarySerializer(serializers.Serializer):
    name = serializers.CharField()
    short_description = serializers.CharField()
    # logo = serializers.ImageField()


class GroupDetailSerializer(serializers.Serializer):
    class Meta:
        model = UserGroup
        field = "__all__"


class GroupApplicationSerializer(serializers.Serializer):
    user_group = serializers.IntegerField
    description = serializers.CharField()
