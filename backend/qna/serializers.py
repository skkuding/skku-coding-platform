from utils.api import UsernameSerializer, serializers
from .models import Question
from course.serializers import CourseSerializer


class QuestionSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    course = CourseSerializer()

    class Meta:
        model = Question
        fields = "__all__"


class CreateQuestionSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    content = serializers.CharField(max_length=1024 * 1024 * 8)


class EditQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    is_open = serializers.BooleanField()


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
