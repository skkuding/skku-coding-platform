from utils.api import APIView
from account.decorators import login_required
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Course, Registration
from ..serializers import CourseStudentSerializer


class CourseAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a course",
                requied=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                description="Number of courses to show",
                type=openapi.TYPE_STRING,
                default=10,
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                description="ID of the first course of list",
                type=openapi.TYPE_STRING,
                default=0,
            ),
        ],
        operation_description="Get registered course list of requesting user",
        responses={200: CourseStudentSerializer},
    )
    @login_required
    def get(self, request):
        course_id = request.GET.get("id")
        user_id = request.user.id

        if not id:
            return self.error("Invalid parameter, id is required")

        if course_id:
            try:
                Course.objects.get(id=course_id)
                course = Registration.objects.get(user_id=user_id, course_id=course_id)
                return self.success(CourseStudentSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")
            except Registration.DoesNotExist:
                return self.error("Invalid access, not registered user")

        courses = Registration.objects.filter(user_id=user_id)

        return self.success(self.paginate_data(request, courses, CourseStudentSerializer))
