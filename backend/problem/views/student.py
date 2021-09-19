from utils.api import APIView
from utils.decorators import check_assignment_permission
from ..models import Problem
from ..serializers import ProblemSafeSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AssignmentProblemAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="assignment_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of assignment",
                required=True
            ),
            openapi.Parameter(
                name="problem_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem",
            )
        ],
        operation_description="Get problem of specific assignment. If \'problem_id\' is not set, whole problems of the assignment would be returned.",
        responses={200: ProblemSafeSerializer},
    )
    @check_assignment_permission()
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by").get(_id=problem_id,
                                                                           assignment=self.assignment,
                                                                           visible=True)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist.")
            return self.success(ProblemSafeSerializer(problem).data)

        assignment_problems = Problem.objects.select_related("created_by").filter(assignment=self.assignment, visible=True)
        return self.success(self.paginate_data(request, assignment_problems, ProblemSafeSerializer))
