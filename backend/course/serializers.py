from django.db.models import fields
from utils.api import UsernameSerializer, serializers
from account.serializers import UserAdminSerializer
from .models import Course, Takes

class CreateCourseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    course_code = serializers.CharField(max_length=64)
    class_number = serializers.IntegerField()
    registered_year = serializers.IntegerField()
    semester = serializers.IntegerField()


class EditCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=64)
    course_code = serializers.CharField(max_length=64)
    class_number = serializers.IntegerField()
    registered_year = serializers.IntegerField()
    semester = serializers.IntegerField()


class RegisterSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    course_id = serializers.IntegerField()


class EditRegisterSerializer(serializers.Serializer):
    registration_id = serializers.IntegerField()
    course_id = serializers.IntegerField()


class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = "__all__"


class CourseProfessorSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = Course
        fields = "__all__"


class CourseStudentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Takes
        fields = ('course',)


class TakesSerializer(serializers.ModelSerializer):
    user = UsernameSerializer()

    class Meta:
        model = Takes
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    user = UserAdminSerializer()

    class Meta:
        model = Takes
        fields = "__all__"