from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.api import APIView, validate_serializer
from utils.constants import CONTEST_PASSWORD_SESSION_KEY
from utils.shortcuts import datetime2str, check_is_id
from account.decorators import login_required, check_contest_permission, check_contest_password

from utils.constants import ContestStatus
from ..models import ContestAnnouncement, Contest
from ..serializers import ContestAnnouncementSerializer
from ..serializers import ContestSerializer, ContestPasswordVerifySerializer


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
        contests = Contest.objects.select_related("created_by").filter(visible=True)
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
