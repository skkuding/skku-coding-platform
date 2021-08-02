from django.http import request
from utils.api import APIView, validate_serializer

from account.models import User

from ..models import Course, Takes
from ..serializers import CourseSerializer, CreateCourseSerializer, CourseListSerializer, RegisterStudentSerializer, TakesSerializer

class CourseAPI(APIView):
    def get(self, request):
        cousre_id = request.GET.get("id")
        if cousre_id:
            try:
                course = Course.objects.get(id=cousre_id)
                return self.success(CourseSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")

        courses = Course.objects.filter(created_by=request.user)
        return self.success(self.paginate_data(request, courses, CourseSerializer))

    @validate_serializer(CreateCourseSerializer)
    def post(self, request):
        data = request.data
        course = Course.objects.create(title=data["title"],
                                        course_code=data["course_code"],
                                        class_number=data["class_number"],
                                        created_by=request.user,
                                        registered_year=data["registered_year"],
                                        semester=data["semester"])
        return self.success(CourseSerializer(course).data)


class StudentManagementAPI(APIView): # params? data? 
    @validate_serializer(RegisterStudentSerializer)
    def post(self, request):
        data = request.data
        course_id = data["course_id"]# request.GET.get('course_id')
        user_id = data["user_id"]# request.GET.get('user_id')

        try:
            Course.objects.get(id=course_id)
            User.objects.get(id=user_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        except User.DoesNotExist:
            return self.error("User does not exist")

        takes = Takes.objects.create(user_id=user_id,
                                    course_id=course_id)
        return self.success(TakesSerializer(takes).data)