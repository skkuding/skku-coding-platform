from utils.api import APIView
from account.decorators import check_assignment_permission
from ..models import Problem
from ..serializers import ProblemSafeSerializer


class AssignmentProblemAPI(APIView):
    @check_assignment_permission(check_type="problems")
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