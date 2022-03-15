from utils.api import serializers


class CreateTemperatureSerializer(serializers.Serializer):
    id = serializers.CharField()
    difficulty = serializers.CharField()
