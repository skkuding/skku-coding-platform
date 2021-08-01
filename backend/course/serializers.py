from django.db.models import fields
from utils.api import UsernameSerializer, serializers

from .models import Course, Takes

class CreateCourseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    course_code = serializers.CharField(max_length=64)
    class_number = serializers.IntegerField()
    registered_year = serializers.IntegerField()
    semester = serializers.IntegerField()


class RegisterStudentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    course_id = serializers.IntegerField()


class CourseSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    data = CourseSerializer(source='course')

    class Meta:
        model = Takes
        fields = ('data',)


class TakesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Takes
        fields = '__all__'