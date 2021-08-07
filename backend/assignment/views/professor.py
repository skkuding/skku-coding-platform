from utils.api import APIView, validate_serializer

from ..models import Assignment
from course.models import Course
from ..serializers import AssginmentProfessorSerializer, CreateAssignmentSerializer, EditAssignmentSerializer

from account.decorators import ensure_created_by, admin_role_required
import dateutil.parser

class AssignmentAPI(APIView):
    @admin_role_required
    def get(self, request):
        assignment_id = request.GET.get("assignment_id")
        course_id = request.GET.get("course_id")

        if not course_id:
            return self.error("Invalid parameter, course_id is required")

        try:
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        if assignment_id:
            try:
                assignment = Assignment.objects.get(id=assignment_id, course_id=course_id)
                return self.success(AssginmentProfessorSerializer(assignment).data)
            except Assignment.DoesNotExist:
                return self.error("Assignment does not exists")

        assignments = Assignment.objects.filter(course_id=course_id)
        return self.success(self.paginate_data(request, assignments, AssginmentProfessorSerializer))
    
    @validate_serializer(CreateAssignmentSerializer)
    @admin_role_required
    def post(self, request):
        data = request.data
        course_id = request.data["course_id"]

        try:
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exists")
        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])
        data["created_by"] = request.user

        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")

        assignment = Assignment.objects.create(**data)
        return self.success(AssginmentProfessorSerializer(assignment).data)
        
    @validate_serializer(EditAssignmentSerializer)
    @admin_role_required
    def put(self, request):
        data = request.data
        try:
            assignment = Assignment.objects.get(id=data.pop("id"))
            ensure_created_by(assignment, request.user)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")

        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])

        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")

        for k, v in data.items():
            setattr(assignment, k, v)
        assignment.save()
        return self.success(AssginmentProfessorSerializer(assignment).data)

    @admin_role_required
    def delete(self, request):
        course_id = request.GET.get("course_id")
        assignment_id = request.GET.get("assignment_id")

        if not course_id:
            return self.error("Invalid parameter, course_id is required")
        if not assignment_id:
            return self.error("Invalid parameter, assignment_id is required")

        try:
            course = Course.objects.get(id=course_id)
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        try:
            assignment = Assignment.objects.get(id=assignment_id)
            ensure_created_by(assignment, request.user)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exists")

        assignment.delete()
        return self.success()
