from django.http import request
from utils.api import APIView, validate_serializer

from ..models import Assignment
from course.models import Course
from ..serializers import AssginmentProfessorSerializer, CreateAssignmentSeriaizer

from account.decorators import ensure_created_by
import dateutil.parser
class AssignmentAPI(APIView):
    def get(self, request):
        assignment_id = request.GET.get('id')
        course_id = request.GET.get('course_id')

        if assignment_id:
            try:
                assignment = Assignment.objects.get(id=assignment_id)
                ensure_created_by(assignment, request.user) # 필요할까?
                return self.success(AssginmentProfessorSerializer(assignment).data)
            except Assignment.DoesNotExist:
                return self.error("Assignment does not exists")

        assignments = Assignment.objects.filter(course_id=course_id)
        return self.success(self.paginate_data(request, assignments, AssginmentProfessorSerializer))
    
    @validate_serializer(CreateAssignmentSeriaizer)
    def post(self, request):
        course_id = request.GET.get("id")
        if course_id:
            try:
                Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return self.error("Course does not exists")
        else:
            return self.error("Parameter error, Course_id is required")

        data = request.data
        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])
        data["created_by"] = request.user

        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")

        assignment = Assignment.objects.create(**data)
        return self.success(AssginmentProfessorSerializer(assignment).data)
        