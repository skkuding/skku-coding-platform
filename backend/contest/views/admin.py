import copy
import os
import zipfile
from ipaddress import ip_network

import dateutil.parser
from django.http import FileResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.models import User
from group.models import Group
from submission.models import Submission, JudgeStatus
from utils.api import APIView, validate_serializer
from utils.cache import cache
from utils.constants import CacheKey
from utils.decorators import ensure_created_by
from utils.shortcuts import rand_str
from utils.tasks import delete_files
from ..models import Contest, ContestAnnouncement, ContestPrize, ACMContestRank
from ..serializers import (ContestAnnouncementSerializer, ContestAdminSerializer,
                           CreateContestSerializer, CreateContestAnnouncementSerializer,
                           EditContestSerializer, EditContestAnnouncementSerializer,
                           ContestPrizeSerializer, ACMContestRankSerializer)


class ContestAPI(APIView):
    @swagger_auto_schema(
        request_body=CreateContestSerializer,
        operation_description="Create new contest",
        responses={200: ContestAdminSerializer},
    )
    @validate_serializer(CreateContestSerializer)
    def post(self, request):
        data = request.data
        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])
        data["created_by"] = request.user
        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")
        if data.get("password") and data["password"] == "":
            data["password"] = None
        for ip_range in data["allowed_ip_ranges"]:
            try:
                ip_network(ip_range, strict=False)
            except ValueError:
                return self.error(f"{ip_range} is not a valid cidr network")
        prizes = data.pop("prizes")
        allowed_groups = data.pop("allowed_groups")
        allowed_groups_qs = Group.objects.filter(id__in=allowed_groups)
        if allowed_groups_qs.count() != len(allowed_groups):
            return self.error("Some groups don't exist")

        contest = Contest.objects.create(**data)
        contest.allowed_groups.set(allowed_groups_qs)
        for prize in prizes:
            ContestPrize.objects.create(contest=contest, **prize)
        data = ContestAdminSerializer(contest).data
        data["prizes"] = ContestPrizeSerializer(ContestPrize.objects.filter(contest=contest), many=True).data
        return self.success(data)

    @swagger_auto_schema(
        request_body=EditContestSerializer,
        operation_description="Edit contest",
        responses={200: ContestAdminSerializer},
    )
    @validate_serializer(EditContestSerializer)
    def put(self, request):
        data = request.data
        try:
            contest = Contest.objects.get(id=data.pop("id"))
            ensure_created_by(contest, request.user)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])
        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")
        if data["password"] == "":
            data["password"] = None
        for ip_range in data["allowed_ip_ranges"]:
            try:
                ip_network(ip_range, strict=False)
            except ValueError:
                return self.error(f"{ip_range} is not a valid cidr network")

        prizes = data.pop("prizes")
        prize_id_list = []
        for item in prizes:
            try:
                if "id" not in item:
                    res = ContestPrize.objects.create(contest=contest, **item)
                    prize_id_list.append(res.id)
                    continue
                prize = ContestPrize.objects.get(contest=contest, id=item["id"])
                prize_id_list.append(item["id"])
                for k, v in item.items():
                    setattr(prize, k, v)
                prize.save()
            except ContestPrize.DoesNotExist:
                item.pop("id")
                res = ContestPrize.objects.create(contest=contest, **item)
                prize_id_list.append(res.id)
        ContestPrize.objects.filter(contest=contest).exclude(id__in=prize_id_list).delete()

        allowed_groups = data.pop("allowed_groups")
        allowed_groups_qs = Group.objects.filter(id__in=allowed_groups)
        if allowed_groups_qs.count() != len(allowed_groups):
            return self.error("Some groups don't exist")
        contest.allowed_groups.set(allowed_groups_qs)
        if not contest.real_time_rank and data.get("real_time_rank"):
            cache_key = f"{CacheKey.contest_rank_cache}:{contest.id}"
            cache.delete(cache_key)

        for k, v in data.items():
            setattr(contest, k, v)

        contest.save()
        data = ContestAdminSerializer(contest).data
        data["prizes"] = ContestPrizeSerializer(ContestPrize.objects.filter(contest=contest), many=True).data
        return self.success(data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a contest",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="keyword",
                in_=openapi.IN_QUERY,
                description="Keyword to be included in contest title",
                type=openapi.TYPE_STRING,
            ),
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
        ],
        operation_description="Get contest list generated by requesting admin",
        responses={200: ContestAdminSerializer},
    )
    def get(self, request):
        contest_id = request.GET.get("id")
        if contest_id:
            try:
                contest = Contest.objects.prefetch_related("prizes").get(id=contest_id)
                ensure_created_by(contest, request.user)
                return self.success(ContestAdminSerializer(contest).data)
            except Contest.DoesNotExist:
                return self.error("Contest does not exist")

        contests = Contest.objects.prefetch_related("prizes").all().order_by("-create_time")
        if request.user.is_admin():
            contests = contests.filter(created_by=request.user)

        keyword = request.GET.get("keyword")
        if keyword:
            contests = contests.filter(title__contains=keyword)
        return self.success(self.paginate_data(request, contests, ContestAdminSerializer))

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Unique ID of a contest",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            contest = Contest.objects.get(id=id)
        except Contest.DoesNotExist:
            return self.error("Contest does not exists")
        ensure_created_by(contest, request.user)

        contest.delete()
        return self.success()


class ContestAnnouncementAPI(APIView):
    @swagger_auto_schema(
        request_body=CreateContestAnnouncementSerializer,
        operation_description="Create one contest announcemnet",
        responses={200: ContestAnnouncementSerializer},
    )
    @validate_serializer(CreateContestAnnouncementSerializer)
    def post(self, request):
        """
        Create one contest_announcement.
        """
        data = request.data
        try:
            contest = Contest.objects.get(id=data.pop("contest_id"))
            ensure_created_by(contest, request.user)
            data["contest"] = contest
            data["created_by"] = request.user
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        announcement = ContestAnnouncement.objects.create(**data)
        return self.success(ContestAnnouncementSerializer(announcement).data)

    @swagger_auto_schema(
        request_body=EditContestAnnouncementSerializer,
        operation_description="Update contest announcement",
        responses={200: ContestAnnouncementSerializer},
    )
    @validate_serializer(EditContestAnnouncementSerializer)
    def put(self, request):
        """
        update contest_announcement
        """
        data = request.data
        try:
            contest_announcement = ContestAnnouncement.objects.get(id=data.pop("id"))
            ensure_created_by(contest_announcement, request.user)
        except ContestAnnouncement.DoesNotExist:
            return self.error("Contest announcement does not exist")
        for k, v in data.items():
            setattr(contest_announcement, k, v)
        contest_announcement.save()
        return self.success(ContestAnnouncementSerializer(contest_announcement).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Id of contest announcement to delete",
                required=True,
                type=openapi.TYPE_INTEGER,
            )
        ],
        operation_description="Delete one contest announcement",
    )
    def delete(self, request):
        """
        Delete one contest_announcement.
        """
        contest_announcement_id = request.GET.get("id")
        if contest_announcement_id:
            if request.user.is_admin():
                ContestAnnouncement.objects.filter(id=contest_announcement_id,
                                                   contest__created_by=request.user).delete()
            else:
                ContestAnnouncement.objects.filter(id=contest_announcement_id).delete()
        return self.success()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="ID of contest announcement",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="contest_id",
                in_=openapi.IN_QUERY,
                description="ID of contest",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="keyword",
                in_=openapi.IN_QUERY,
                description="Keyword to be included in contest title",
                type=openapi.TYPE_STRING,
            ),
        ],
        operation_description="Get single contest announcement or contest announcement list"
    )
    def get(self, request):
        """
        Get one contest_announcement or contest_announcement list.
        """
        contest_announcement_id = request.GET.get("id")
        if contest_announcement_id:
            try:
                contest_announcement = ContestAnnouncement.objects.get(id=contest_announcement_id)
                ensure_created_by(contest_announcement, request.user)
                return self.success(ContestAnnouncementSerializer(contest_announcement).data)
            except ContestAnnouncement.DoesNotExist:
                return self.error("Contest announcement does not exist")

        contest_id = request.GET.get("contest_id")
        if not contest_id:
            return self.error("Parameter error")
        contest_announcements = ContestAnnouncement.objects.filter(contest_id=contest_id)
        if request.user.is_admin():
            contest_announcements = contest_announcements.filter(created_by=request.user)
        keyword = request.GET.get("keyword")
        if keyword:
            contest_announcements = contest_announcements.filter(title__contains=keyword)
        return self.success(ContestAnnouncementSerializer(contest_announcements, many=True).data)


class ContestRankAPI(APIView):
    def put(self, request):
        """
        update contest_rank Prize
        """
        data = request.data
        try:
            contest_rank = ACMContestRank.objects.get(id=data.pop("id"))
        except ACMContestRank.DoesNotExist:
            return self.error("ACM contest rank does not exist")
        contest_rank.prize = ContestPrize.objects.get(id=data["prize_id"])
        contest_rank.save()
        return self.success(ACMContestRankSerializer(contest_rank).data)


class DownloadContestSubmissions(APIView):
    def _dump_submissions(self, contest, exclude_admin=True):
        problem_ids = contest.problem_set.all().values_list("id", "_id")
        id2display_id = {k[0]: k[1] for k in problem_ids}
        ac_map = {k[0]: False for k in problem_ids}
        submissions = Submission.objects.filter(contest=contest, result=JudgeStatus.ACCEPTED).order_by("-create_time")
        user_ids = submissions.values_list("user_id", flat=True)
        users = User.objects.filter(id__in=user_ids)
        path = f"/tmp/{rand_str()}.zip"
        with zipfile.ZipFile(path, "w") as zip_file:
            for user in users:
                if user.is_admin_role() and exclude_admin:
                    continue
                user_ac_map = copy.deepcopy(ac_map)
                user_submissions = submissions.filter(user_id=user.id)
                for submission in user_submissions:
                    problem_id = submission.problem_id
                    if user_ac_map[problem_id]:
                        continue
                    file_name = f"{user.username}_{id2display_id[submission.problem_id]}.txt"
                    compression = zipfile.ZIP_DEFLATED
                    zip_file.writestr(zinfo_or_arcname=f"{file_name}",
                                      data=submission.code,
                                      compress_type=compression)
                    user_ac_map[problem_id] = True
        return path

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="contest_id",
                in_=openapi.IN_QUERY,
                description="ID of contest",
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="exclude_admin",
                in_=openapi.IN_QUERY,
                description="Set value '1' to exclude admin",
                type=openapi.TYPE_STRING,
            ),
        ],
        operation_description="Download submissions of single contest",
    )
    def get(self, request):
        contest_id = request.GET.get("contest_id")
        if not contest_id:
            return self.error("Parameter error")
        try:
            contest = Contest.objects.get(id=contest_id)
            ensure_created_by(contest, request.user)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")

        exclude_admin = request.GET.get("exclude_admin") == "1"
        zip_path = self._dump_submissions(contest, exclude_admin)
        delete_files.send_with_options(args=(zip_path,), delay=300_000)
        resp = FileResponse(open(zip_path, "rb"))
        resp["Content-Type"] = "application/zip"
        resp["Content-Disposition"] = f"attachment;filename={os.path.basename(zip_path)}"
        return resp
