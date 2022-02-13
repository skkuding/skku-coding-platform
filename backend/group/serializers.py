from .models import GroupMemberJoin, GroupMember, GroupRegistrationRequest, Group
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


class CreateGroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    is_official = serializers.BooleanField()


class GroupSummarySerializer(serializers.ModelSerializer):
    # logo = serializers.ImageField()

    class Meta:
        model = Group
        fields = ["name", "short_description", "id"]


class GroupDetailSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = Group
        fields = "__all__"


class CreateGroupMemberJoinSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    description = serializers.CharField()


class GroupMemberJoinSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = GroupMemberJoin
        fields = "__all__"


class EditGroupMemberPermissionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    is_group_admin = serializers.BooleanField()


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UsernameSerializer()

    class Meta:
        model = GroupMember
        fields = "__all__"
