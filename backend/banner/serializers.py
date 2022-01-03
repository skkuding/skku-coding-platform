from utils.api import serializers

from .models import Banner


class BannerSerializer(serializers.Serializer):
    path = serializers.CharField(max_length=1024)


class BannerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class CreateBannerSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    path = serializers.CharField(max_length=1024)


class EditBannerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    path = serializers.CharField()
    visible = serializers.BooleanField()
