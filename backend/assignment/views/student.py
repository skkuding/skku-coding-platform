from utils.api import APIView
from utils.decorators import login_required

from course.models import Course, Registration

from ..models import Assignment
from ..serializers import AssignmentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AssignmentAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="course_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a course",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="assignment_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a assignment",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                description="Number of assignments to show",
                type=openapi.TYPE_STRING,
                default=10,
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                description="ID of the first assignment of list",
                type=openapi.TYPE_STRING,
                default=0,
            ),
        ],
        operation_description="Get assignment list of the course",
        responses={200: AssignmentSerializer},
    )
    @login_required
    def get(self, request):
        assignment_id = request.GET.get("assignment_id")
        course_id = request.GET.get("course_id")

        if not course_id:
            return self.error("Invalid parameter, course_id is required")

        try:
            Course.objects.get(id=course_id)
            Registration.objects.get(user_id=request.user.id, course_id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        except Registration.DoesNotExist:
            return self.error("Invalid access, not registered user")

        context = {"request": request}

        if assignment_id:
            try:
                assignment = Assignment.objects.get(id=assignment_id, course_id=course_id, visible=True)
                return self.success(AssignmentSerializer(assignment, context=context).data)
            except Assignment.DoesNotExist:
                return self.error("Assignment does not exists")

        assignments = Assignment.objects.filter(course_id=course_id, visible=True)
        return self.success(self.paginate_data(request, assignments, AssignmentSerializer, context))
