from utils.api import serializers
from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    admin_type = serializers.CharField()
    content = serializers.CharField()
    last_update_time = serializers.DateTimeField()

class CreateAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    content = serializers.CharField()

class EditAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
