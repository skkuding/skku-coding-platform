from django.utils.timezone import now
from django.core.cache import cache
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.api import APIView, validate_serializer
from utils.constants import CacheKey, CONTEST_PASSWORD_SESSION_KEY
from utils.shortcuts import datetime2str, check_is_id
from account.models import AdminType
from utils.decorators import login_required, check_contest_permission, check_contest_password

from utils.constants import ContestStatus
from ..models import ContestAnnouncement, Contest, ACMContestRank, ProblemBank
from problem.models import Problem
from ..serializers import ACMContestRankNoPenaltySerializer, ContestAnnouncementSerializer
from ..serializers import ContestSerializer, ContestPasswordVerifySerializer
from ..serializers import ACMContestRankSerializer

import random
import json


class ContestAnnouncementListAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="contest_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a contest",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="max_id",
                in_=openapi.IN_QUERY,
                description="Get announcements whose IDs are greater than `max_id`",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        operation_description="Get contest announcement list",
    )
    @check_contest_permission(check_type="announcements")
    def get(self, request):
        contest_id = request.GET.get("contest_id")
        if not contest_id:
            return self.error("Invalid parameter, contest_id is required")
        data = ContestAnnouncement.objects.select_related("created_by").filter(contest_id=contest_id, visible=True)
        max_id = request.GET.get("max_id")
        if max_id:
            data = data.filter(id__gt=max_id)
        return self.success(ContestAnnouncementSerializer(data, many=True).data)


class ContestAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a contest",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        opearation_description="Get single contest information",
    )
    def get(self, request):
        id = request.GET.get("id")
        if not id or not check_is_id(id):
            return self.error("Invalid parameter, id is required")
        try:
            contest = Contest.objects.get(id=id, visible=True)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        data = ContestSerializer(contest).data
        data["now"] = datetime2str(now())
        return self.success(data)


class ContestListAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                description="Number of contests to show",
                type=openapi.TYPE_STRING,
                default=10,
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                description="ID of the first contest of list",
                type=openapi.TYPE_STRING,
                default=0,
            ),
            openapi.Parameter(
                name="keyword",
                in_=openapi.IN_QUERY,
                description="Keyword to be included in contest title",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="rule_type",
                in_=openapi.IN_QUERY,
                description="Rule type ('ACM' or 'OI')",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="status",
                in_=openapi.IN_QUERY,
                description="Contest status (NOT_START(1), UNDERWAY(0), ENDED(-1))",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        # responses=ContestSerializer(many=True),
        operation_description="Get contest list from <`offset`> to <`offset`+`limit`>",
    )
    def get(self, request):
        contests = Contest.objects.select_related("created_by").filter(visible=True).annotate(participants_count=Count("acmcontestrank"))
        keyword = request.GET.get("keyword")
        rule_type = request.GET.get("rule_type")
        status = request.GET.get("status")
        if keyword:
            contests = contests.filter(title__contains=keyword)
        if rule_type:
            contests = contests.filter(rule_type=rule_type)
        if status:
            cur = now()
            if status == ContestStatus.CONTEST_NOT_START:
                contests = contests.filter(start_time__gt=cur)
            elif status == ContestStatus.CONTEST_ENDED:
                contests = contests.filter(end_time__lt=cur)
            else:
                contests = contests.filter(start_time__lte=cur, end_time__gte=cur)
        return self.success(self.paginate_data(request, contests, ContestSerializer))


class ContestPasswordVerifyAPI(APIView):
    @swagger_auto_schema(
        request_body=ContestPasswordVerifySerializer,
        operation_description="Verify contest password",
    )
    @validate_serializer(ContestPasswordVerifySerializer)
    @login_required
    def post(self, request):
        data = request.data
        try:
            contest = Contest.objects.get(id=data["contest_id"], visible=True, password__isnull=False)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        if not check_contest_password(data["password"], contest.password):
            return self.error("Wrong password or password expired")

        # password verify OK.
        if CONTEST_PASSWORD_SESSION_KEY not in request.session:
            request.session[CONTEST_PASSWORD_SESSION_KEY] = {}
        request.session[CONTEST_PASSWORD_SESSION_KEY][contest.id] = data["password"]
        # https://docs.djangoproject.com/en/dev/topics/http/sessions/#when-sessions-are-saved
        request.session.modified = True
        return self.success(True)


class ContestAccessAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="contest_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a contest",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        operation_description="Check access permission to a contest",
    )
    @login_required
    def get(self, request):
        contest_id = request.GET.get("contest_id")
        if not contest_id:
            return self.error()
        try:
            contest = Contest.objects.get(id=contest_id, visible=True, password__isnull=False)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        session_pass = request.session.get(CONTEST_PASSWORD_SESSION_KEY, {}).get(contest.id)
        return self.success({"access": check_contest_password(session_pass, contest.password)})


class ContestRankAPI(APIView):
    def get_rank(self):
        return ACMContestRank.objects.filter(contest=self.contest, user__admin_type=AdminType.REGULAR_USER, user__is_disabled=False).\
            select_related("user").order_by("-accepted_number", "total_penalty", "total_time")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="contest_id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a contest",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        operation_description="Check access permission to a contest",
    )
    @login_required
    @check_contest_permission(check_type="ranks")
    def get(self, request):
        contest_id = request.GET.get("contest_id")
        try:
            contest = Contest.objects.get(id=contest_id, visible=True)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        self.contest = contest
        force_refresh = request.GET.get("force_refresh")
        is_contest_admin = request.user.is_authenticated and request.user.is_contest_admin(contest)
        serializer = ACMContestRankSerializer if contest.rank_penalty_visible else ACMContestRankNoPenaltySerializer

        if force_refresh == "1":
            qs = self.get_rank()
        else:
            cache_key = f"{CacheKey.contest_rank_cache}:{contest_id}"
            qs = cache.get(cache_key)
            if not qs:
                qs = self.get_rank()
                cache.set(cache_key, qs)

        page_qs = self.paginate_data(request, qs)
        if(len(page_qs["results"]) != 0):
            page_qs["results"] = serializer(page_qs["results"], many=True, is_contest_admin=is_contest_admin).data
        else:
            page_qs["results"] = serializer(page_qs["results"], many=True, is_contest_admin=is_contest_admin).data
            page_qs["results"].append(self.contest.id)
        return self.success(page_qs)


class ProblemBankAPI(APIView):
    @login_required
    @check_contest_permission(check_type="problems")
    def post(self, request):
        # Contest 참가하기 -> ProblemBank Post
        data = request.data
        try:
            contest = Contest.objects.get(id=data["contest_id"])
        except Contest.DoesNotExist:
            return self.error("Contest Does not exist")

        bank_filter = contest.bank_filter

        # filtered random problem list
        problem_list = []

        for data in bank_filter:
            problems = list(Problem.objects.filter(difficulty=data["level"], bank=True).values_list("id", flat=True))
            random_problems = random.sample(problems, data["count"])
            problem_list.extend(random_problems)

        problem_bank = ProblemBank.objects.create(contest=contest, user=request.user)
        problem_bank.problem_list = json.dumps(problem_list)
        problem_bank.save()
        return self.success()

    @login_required
    @check_contest_permission(check_type="problems")
    def get(self, request):
        # Contest 참가하는지 확인 -> ProblemBank Get
        data = request.data
        try:
            contest = Contest.objects.get(id=data["contest_id"])
        except Contest.DoesNotExist:
            return self.error("Contest Does not exist")

        try:
            ProblemBank.objects.get(contest=contest, user=request.user)
        except ProblemBank.DoesNotExist:
            return self.success(False)
        return self.success(True)
