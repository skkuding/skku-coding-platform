from django.http import request
from utils.api import UsernameSerializer, APIView

from ..models import Assignment
from ..serializers import AssignmentSerializer

class AssignmentAPI(APIView):
    def get(self, request):
        assignment_id = request.GET.get("id")
        course_id = request.GET.get("course_id")

        if assignment_id:
            try:
                assignment = Assignment.objects.get(id=assignment_id, visible=True)
                return self.success(AssignmentSerializer(assignment).data)
            except Assignment.DoesNotExist:
                return self.error("Assignment does not exists")

        assignments = Assignment.objects.filter(course_id=course_id)

        assignment_list = [assignment.id for assignment in assignments]
        

        return self.success(self.paginate_data(request, assignments, AssignmentSerializer))