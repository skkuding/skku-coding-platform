from django.db.models import fields
from utils.api import UsernameSerializer, serializers

from .models import Assignment
from submission.models import Submission
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
    total_problem = serializers.SerializerMethodField(read_only=True)
    submitted_problem = serializers.SerializerMethodField(read_only=True)

    def get_total_problem(self, obj):
        return obj.problems.count()

    def get_submitted_problem(self, obj):
        return Submission.objects.filter(assignment=obj, user_id=obj.created_by).count()
        # return obj.submissions.filter(user_id=obj.creatd_by).count()

    class Meta:
        model = Assignment
        fields = "__all__"


class CreateAssignmentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    # course = serializers.IntegerField()
    content = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()