from django.db.models import Q, Count
from utils.api import APIView
from utils.decorators import check_contest_permission
from ..models import ProblemSet, ProblemSetGroup, ProblemTag, Problem, ProblemRuleType
from ..serializers import ProblemSerializer, ProblemSetGroupSerializer, ProblemSetSerializer, TagSerializer, ProblemSafeSerializer, BankProblemSerializer
from contest.models import ContestRuleType, ProblemBank
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import json


class ProblemTagAPI(APIView):
    @swagger_auto_schema(
        operation_description="Pick a set of problems that contain certain tag.",
        responses={200: TagSerializer}
    )
    def get(self, request):
        tags = ProblemTag.objects.annotate(problem_count=Count("problem")).filter(problem_count__gt=0)
        return self.success(TagSerializer(tags, many=True).data)


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
                    .get(_id=problem_id, contest_id__isnull=True, assignment_id__isnull=True, visible=True, bank=False)
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, problem_data)
                return self.success(problem_data)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        limit = request.GET.get("limit")
        if not limit:
            return self.error("Limit is needed")

        problems = Problem.objects.select_related("created_by").filter(contest_id__isnull=True, assignment_id__isnull=True, visible=True, bank=False)

        problem_set_id = request.GET.get("problem_set_id")
        if problem_set_id:
            try:
                problem_set = ProblemSet.objects.get(id=problem_set_id)
            except ProblemSet.DoesNotExist:
                return self.error("Problem set does not exist.")
            problems = problems.filter(problem_set=problem_set)
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


class BankProblemAPI(APIView):
    @check_contest_permission(check_type="problems")
    def get(self, request):
        if not self.contest.is_bank:
            return self.error("This is not a problem bank contest")

        try:
            problem_bank = ProblemBank.objects.get(user=request.user, contest=self.contest)
        except ProblemBank.DoesNotExist:
            return self.error("You don't have permission of this contest")

        decoder = json.decoder.JSONDecoder()
        bank_problem_ids = decoder.decode(problem_bank.problem_list)

        problem_id = request.GET.get("problem_id")
        if problem_id:
            if int(problem_id) not in bank_problem_ids:
                return self.error("This problem is not allocated to you")
            try:
                problem = Problem.objects.select_related("created_by") \
                    .get(_id=problem_id, contest_id__isnull=True, assignment_id__isnull=True)
                data = BankProblemSerializer(problem).data
                return self.success(data)
            except Problem.DoesNotExist:
                return self.error("Problem does not eixst")

        problems = Problem.objects.select_related("created_by").filter(pk__in=bank_problem_ids)
        data = BankProblemSerializer(problems, many=True).data
        return self.success(data)


class ProblemSetGroupAPI(APIView):
    def get(self, request):
        id = request.GET.get("id")

        if not id:
            problem_set_group = ProblemSetGroup.objects.filter(is_disabled=False)
            return self.success(ProblemSetGroupSerializer(problem_set_group, many=True).data)

        try:
            problem_set_group = ProblemSetGroup.objects.get(id=id, is_disabled=False)
            return self.success(ProblemSetGroupSerializer(problem_set_group).data)
        except ProblemSetGroup.DoesNotExist:
            return self.error("Problem set group does not exist.")


class ProblemSetAPI(APIView):
    def get(self, request):
        id = request.GET.get("id")
        problem_set_group_id = request.GET.get("problem_set_group_id")

        if not problem_set_group_id:
            return self.error("Problem set group id is required.")

        try:
            problem_set_group = ProblemSetGroup.objects.get(id=problem_set_group_id, is_disabled=False)
        except ProblemSetGroup.DoesNotExist:
            return self.error("Problem set group does not exist")

        if not id:
            problem_set = ProblemSet.objects.filter(problem_set_group=problem_set_group, is_disabled=False, is_public=True)
            return self.success(ProblemSetSerializer(problem_set, many=True).data)

        try:
            problem_set = ProblemSet.objects.get(problem_set_group=problem_set_group, id=id, is_disabled=False, is_public=True)
            return self.success(ProblemSetSerializer(problem_set).data)
        except ProblemSet.DoesNotExist:
            return self.error("Problem set does not exist.")
