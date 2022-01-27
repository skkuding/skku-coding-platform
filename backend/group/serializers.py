from utils.api import serializers


class CreateUserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    description = serializers.CharField()
    logo = serializers.ImageField()

class GroupApplication(serializers.Serializer):
    user_group = serializers.IntegerField
    description = serializers.CharField()
