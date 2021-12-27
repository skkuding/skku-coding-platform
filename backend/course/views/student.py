from utils.api import APIView, validate_serializer
from utils.decorators import login_required
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Course, Registration
from ..serializers import BookmarkCourseSerializer, CourseRegistrationSerializer


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
                name="bookmark",
                in_=openapi.IN_QUERY,
                description="True for get bookmark list",
                type=openapi.TYPE_BOOLEAN
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
        responses={200: CourseRegistrationSerializer},
    )
    @login_required
    def get(self, request):
        course_id = request.GET.get("id")
        user_id = request.user.id

        if course_id:
            try:
                Course.objects.get(id=course_id)
                course = Registration.objects.get(user_id=user_id, course_id=course_id)
                return self.success(CourseRegistrationSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")
            except Registration.DoesNotExist:
                return self.error("Invalid access, not registered user")

        courses = Registration.objects.filter(user_id=user_id)

        if request.GET.get("bookmark") == "true":
            courses = courses.filter(bookmark=True)

        return self.success(self.paginate_data(request, courses, CourseRegistrationSerializer))


class BookmarkCourseAPI(APIView):
    @swagger_auto_schema(
        request_body=BookmarkCourseSerializer,
        operation_description="Bookmark a course"
    )
    @validate_serializer(BookmarkCourseSerializer)
    @login_required
    def put(self, request):
        data = request.data
        course_id = data["course_id"]

        try:
            Course.objects.get(id=course_id)
            registration = Registration.objects.get(user_id=request.user.id, course_id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        except Registration.DoesNotExist:
            return self.error("Invalid access, not registered course")

        registration.bookmark = data["bookmark"]

        registration.save()
        return self.success(BookmarkCourseSerializer(registration).data)
