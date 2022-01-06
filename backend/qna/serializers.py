from utils.api import UsernameSerializer, serializers
from .models import Question, Answer
from course.serializers import CourseSerializer

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
      fields = ("title", "content","last_update_time")