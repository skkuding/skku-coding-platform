from .models import GroupApplication, GroupRegistrationRequest, UserGroup
from utils.api import serializers, UsernameSerializer


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


class GroupRegistrationResponseSerializer(serializers.Serializer):
    accept = serializers.BooleanField()
    request_id = serializers.IntegerField()
    # logo = serializers.ImageField()


class GroupSummarySerializer(serializers.Serializer):
    name = serializers.CharField()
    short_description = serializers.CharField()
    # logo = serializers.ImageField()


class GroupDetailSerializer(serializers.ModelSerializer):
    members = UsernameSerializer(many=True)
    admin_members = UsernameSerializer(many=True)
    created_by = UsernameSerializer()

    class Meta:
        model = UserGroup
        fields = "__all__"


class CreateGroupApplicationSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    description = serializers.CharField()


class GroupApplicationSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = GroupApplication
        fields = "__all__"
