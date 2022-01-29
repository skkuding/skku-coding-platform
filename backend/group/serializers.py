from .models import GroupRegistrationRequest, UserGroup
from utils.api import serializers


class CreateGroupRegistrationRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    is_official = serializers.BooleanField()
    # logo = serializers.ImageField()


class GroupRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRegistrationRequest
        fields = "__all__"


class CreateGroupSerializer(serializers.Serializer):
    accept = serializers.BooleanField()
    request_id = serializers.IntegerField()
    # logo = serializers.ImageField()


class GroupSummarySerializer(serializers.Serializer):
    name = serializers.CharField()
    short_description = serializers.CharField()
    # logo = serializers.ImageField()


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = "__all__"


class GroupApplicationSerializer(serializers.Serializer):
    user_group = serializers.IntegerField
    description = serializers.CharField()
