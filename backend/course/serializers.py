from utils.api import UsernameSerializer, serializers
from account.serializers import UserAdminSerializer
from .models import Course, Registration


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
    username = serializers.ListField(child=serializers.CharField(), allow_empty=False, min_length=1, max_length=None)
    course_id = serializers.IntegerField()


class EditRegisterSerializer(serializers.Serializer):
    registration_id = serializers.IntegerField()
    course_id = serializers.IntegerField()


class RegisterErrorSerializer(serializers.Serializer):
    user_not_exist = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    already_registered_user = serializers.ListField(child=serializers.CharField(), allow_empty=True)


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseUsernameSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer(need_real_name=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseProfessorSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()

    class Meta:
        model = Course
        fields = "__all__"


class CourseRegistrationSerializer(serializers.ModelSerializer):
    course = CourseUsernameSerializer()

    class Meta:
        model = Registration
        fields = ("course", "bookmark",)


class BookmarkCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    bookmark = serializers.BooleanField()


class UserListSerializer(serializers.ModelSerializer):
    user = UserAdminSerializer()

    class Meta:
        model = Registration
        fields = "__all__"
