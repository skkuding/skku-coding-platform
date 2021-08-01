from django.db.models import fields
from utils.api import UsernameSerializer, serializers

from .models import Assignment
from problem.serializers import BaseProblemSerializer
from problem.serializers import ProblemSerializer
class AssginmentProfessorSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    status = serializers.CharField()
    class Meta:
        model = Assignment
        fields = "__all__"

class AssignmentSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    problems = ProblemSerializer(read_only=True, many=True) # 테스트 필요, 되면 개수 count
    class Meta:
        model = Assignment
        fields = "__all__"


class CreateAssignmentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    # course = serializers.IntegerField()
    content = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()