from utils.api import UsernameSerializer, serializers
from .models import Question, Answer
from course.serializers import CourseSerializer


class QuestionSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    course = CourseSerializer()
    class Meta:
        model = Question
        fields = "__all__"

class CreateQuestionSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    # created_by = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    last_update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()

class EditQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    content = serializers.CharField(max_length=1024 * 1024 * 8)

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