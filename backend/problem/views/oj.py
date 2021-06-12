import random
from django.db.models import Q, Count
from utils.api import APIView
from utils.decorators import check_contest_permission
from ..models import ProblemTag, Problem, ProblemRuleType
from ..serializers import ProblemSerializer, TagSerializer, ProblemSafeSerializer
from contest.models import ContestRuleType
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProblemTagAPI(APIView):
    @swagger_auto_schema(
        operation_description="Pick a set of problems that contain certain tag.",
        responses=TagSerializer
    )
    def get(self, request):
        tags = ProblemTag.objects.annotate(problem_count=Count("problem")).filter(problem_count__gt=0)
        return self.success(TagSerializer(tags, many=True).data)


class PickOneAPI(APIView):
    @swagger_auto_schema(
        operation_description="Pick one problem arbitrarily",
    )
    def get(self, request):
        problems = Problem.objects.filter(contest_id__isnull=True, visible=True)
        count = problems.count()
        if count == 0:
            return self.error("No problem to pick")
        return self.success(problems[random.randint(0, count - 1)]._id)


class ProblemAPI(APIView):
    @staticmethod
    def _add_problem_status(request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            acm_problems_status = profile.acm_problems_status.get("problems", {})
            oi_problems_status = profile.oi_problems_status.get("problems", {})
            # paginate data
            results = queryset_values.get("results")
            if results is not None:
                problems = results
            else:
                problems = [queryset_values, ]
            for problem in problems:
                if problem["rule_type"] == ProblemRuleType.ACM:
                    problem["my_status"] = acm_problems_status.get(str(problem["id"]), {}).get("status")
                else:
                    problem["my_status"] = oi_problems_status.get(str(problem["id"]), {}).get("status")

    @swagger_auto_schema(
        operation_description="Get problems that satisfy specific condition(id, tag, keyword and so on..)",
        manual_parameters=[
            openapi.Parameter(
                name="problem_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem. It set, a specific problem is returned.",
            ),
            openapi.Parameter(
                name="limit", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Maximun number of problem list. Working when \'problem_id\' is not set.",
            ),
            openapi.Parameter(
                name="offset", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Start number of the problem in the list.",
            ),
            openapi.Parameter(
                name="tag", in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Tag of problem you want to search with.",
            ),
            openapi.Parameter(
                name="keyword", in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Keyword of problem\'s title you want to search with.",
            ),
            openapi.Parameter(
                name="difficulty", in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Difficulty of problem you want to search with.",
            ),
        ],
    )
    def get(self, request):
        #  question details page
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by") \
                    .get(_id=problem_id, contest_id__isnull=True, visible=True)
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, problem_data)
                return self.success(problem_data)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        limit = request.GET.get("limit")
        if not limit:
            return self.error("Limit is needed")

        problems = Problem.objects.select_related("created_by").filter(contest_id__isnull=True, visible=True)
        # filter by label
        tag_text = request.GET.get("tag")
        if tag_text:
            problems = problems.filter(tags__name=tag_text)

        # search situation
        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            problems = problems.filter(Q(title__icontains=keyword) | Q(_id__icontains=keyword))

        # difficulty screening
        difficulty = request.GET.get("difficulty")
        if difficulty:
            problems = problems.filter(difficulty=difficulty)

        # Add tags to the topics that have been done according to the profile
        data = self.paginate_data(request, problems, ProblemSerializer)
        self._add_problem_status(request, data)
        return self.success(data)


class ContestProblemAPI(APIView):
    def _add_problem_status(self, request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            if self.contest.rule_type == ContestRuleType.ACM:
                problems_status = profile.acm_problems_status.get("contest_problems", {})
            else:
                problems_status = profile.oi_problems_status.get("contest_problems", {})
            for problem in queryset_values:
                problem["my_status"] = problems_status.get(str(problem["id"]), {}).get("status")

    @check_contest_permission(check_type="problems")
    @swagger_auto_schema(
        operation_description="Get problem of specific contest. If \'problem_id\' is not set, whole problems of the contest would be returned.",
        manual_parameters=[
            openapi.Parameter(
                name="contest_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of contest",
                required=True
            ),
            openapi.Parameter(
                name="problem_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem",
            )
        ]
    )
    @check_contest_permission(check_type="problems")
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by").get(_id=problem_id,
                                                                           contest=self.contest,
                                                                           visible=True)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist.")
            if self.contest.problem_details_permission(request.user):
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, [problem_data, ])
            else:
                problem_data = ProblemSafeSerializer(problem).data
            return self.success(problem_data)

        contest_problems = Problem.objects.select_related("created_by").filter(contest=self.contest, visible=True)
        if self.contest.problem_details_permission(request.user):
            data = ProblemSerializer(contest_problems, many=True).data
            self._add_problem_status(request, data)
        else:
            data = ProblemSafeSerializer(contest_problems, many=True).data
        return self.success(data)
