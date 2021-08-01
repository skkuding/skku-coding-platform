from django.http import request
from utils.api import APIView, validate_serializer

from ..models import Course, Takes
from ..serializers import CourseSerializer, CreateCourseSerializer, CourseListSerializer, RegisterStudentSerializer, TakesSerializer

class CourseAPI(APIView):
    def get(self, request):
        cousre_id = request.GET.get("id")
        user_id = request.GET.get("user_id")
        if cousre_id:
            try:
                course = Course.objects.get(id=cousre_id)
                return self.success(CourseSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Contest does not exist")

        courses = Takes.objects.filter(user_id=user_id)
        return self.success(self.paginate_data(request, courses, CourseListSerializer))

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


class StudentManagementAPI(APIView):
    @validate_serializer(RegisterStudentSerializer)
    def post(self, request):
        data = request.data
        takes = Takes.objects.create(user_id=data['user_id'],
                                        course_id=data['course_id'])
        return self.success(TakesSerializer(takes).data)