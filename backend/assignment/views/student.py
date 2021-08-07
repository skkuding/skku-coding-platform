from utils.api import APIView
from account.decorators import login_required

from course.models import Course, Takes

from ..models import Assignment
from ..serializers import AssignmentSerializer

class AssignmentAPI(APIView):
    @login_required
    def get(self, request):
        assignment_id = request.GET.get("assignment_id")
        course_id = request.GET.get("course_id")

        if not course_id:
            return self.error("Invalid parameter, course_id is required")

        try:
            Course.objects.get(id=course_id)
            Takes.objects.get(user_id=request.user.id, course_id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        except Takes.DoesNotExist:
            return self.error("Invalid access, not registered user")

        context = {"request": request}

        if assignment_id:
            try:
                assignment = Assignment.objects.get(id=assignment_id, course_id=course_id, visible=True)
                return self.success(AssignmentSerializer(assignment, context=context).data)
            except Assignment.DoesNotExist:
                return self.error("Assignment does not exists")

        assignments = Assignment.objects.filter(course_id=course_id)
        return self.success(self.paginate_data(request, assignments, AssignmentSerializer, context))