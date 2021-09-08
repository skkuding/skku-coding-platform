from utils.api import UsernameSerializer, serializers

from .models import Assignment
from submission.models import Submission
from course.serializers import CourseSerializer


class AssignmentProfessorSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    course = CourseSerializer()
    status = serializers.CharField()

    class Meta:
        model = Assignment
        fields = "__all__"


class AssignmentSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    total_problem = serializers.SerializerMethodField(read_only=True)
    submitted_problem = serializers.SerializerMethodField(read_only=True)
    accepted_problem = serializers.SerializerMethodField(read_only=True)

    def get_total_problem(self, obj):
        return obj.problems.count()

    def get_submitted_problem(self, obj):
        user = self.context["request"].user
        return Submission.objects.filter(assignment=obj, user_id=user.id).values("problem").distinct().count()

    def get_accepted_problem(self, obj):
        user = self.context["request"].user
        return Submission.objects.filter(assignment=obj, user_id=user.id, result=0).values("problem").distinct().count()

    class Meta:
        model = Assignment
        exclude = ("created_by", "visible", "create_time", "last_update_time", "course")


class AssignmentCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Assignment
        exclude = ("created_by", "content", "start_time", "end_time", "create_time", "last_update_time", "visible")


class CreateAssignmentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    course_id = serializers.IntegerField()
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    visible = serializers.BooleanField()


class EditAssignmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=128)
    course_id = serializers.IntegerField()
    content = serializers.CharField(max_length=1024 * 1024 * 8)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    visible = serializers.BooleanField()
