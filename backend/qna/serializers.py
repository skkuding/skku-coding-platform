from utils.api import UsernameSerializer, serializers
from .models import Question, Answer
from course.serializers import CourseSerializer


class QuestionSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    course = CourseSerializer()

    class Meta:
        model = Question
        fields = "__all__"

class CreateQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = "__all__"

class EditQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Question
        fields = ("title", "content")


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    admin_type = serializers.CharField()
    content = serializers.CharField()
    last_update_time = serializers.DateTimeField()

class CreateAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    content = serializers.CharField()
    closure = serializers.BooleanField()

class EditAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()