from utils.api import APIView
from utils.api import validate_serializer
from utils.constants import AssignmentStatus
from utils.decorators import ensure_created_by, admin_role_required

from submission.models import Submission
from assignment.models import Assignment
from .admin import ProblemBase

from ..models import Problem, ProblemRuleType, ProblemTag
from ..serializers import (CreateAssignmentProblemSerializer, ProblemAdminSerializer, AddAssignmentProblemSerializer,
                           ProblemProfessorSerializer, EditAssignmentProblemSerializer)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AssignmentProblemAPI(ProblemBase):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="problem_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem.",
            ),
            openapi.Parameter(
                name="assignment_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Unique id of assignment.",
            ),
        ],
        operation_description="Get problems of certain assignment. If problem_id is set, certain problem would be returned.",
        responses={200: ProblemProfessorSerializer},
    )
    @admin_role_required
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        assignment_id = request.GET.get("assignment_id")
        user = request.user
        if problem_id:
            try:
                problem = Problem.objects.get(id=problem_id)
                ensure_created_by(problem.assignment, user)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")
            return self.success(ProblemProfessorSerializer(problem).data)

        if not assignment_id:
            return self.error("Invalid parameter, assignment id is required")
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            ensure_created_by(assignment, user)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")

        problems = Problem.objects.filter(assignment=assignment).order_by("create_time")
        return self.success(self.paginate_data(request, problems, ProblemProfessorSerializer))

    @swagger_auto_schema(
        request_body=(CreateAssignmentProblemSerializer),
        operation_description="Create a problem of assignment.",
        responses={200: ProblemAdminSerializer},
    )
    @validate_serializer(CreateAssignmentProblemSerializer)
    @admin_role_required
    def post(self, request):
        data = request.data
        try:
            assignment = Assignment.objects.get(id=data.pop("assignment_id"))
            ensure_created_by(assignment, request.user)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")
        if assignment.status == AssignmentStatus.ASSIGNMENT_ENDED:
            return self.error("Assignment deadline has expired")

        _id = data["_id"]

        if Problem.objects.filter(_id=_id, assignment=assignment).exists():
            return self.error("Duplicate Display id")

        error_info = self.common_checks(request)
        if error_info:
            return self.error(error_info)

        data["assignment"] = assignment
        tags = data.pop("tags")
        data["created_by"] = request.user
        problem = Problem.objects.create(**data)

        if not _id:
            problem._id = problem.id
            problem.save()

        for item in tags:
            try:
                tag = ProblemTag.objects.get(name=item)
            except ProblemTag.DoesNotExist:
                tag = ProblemTag.objects.create(name=item)
            problem.tags.add(tag)
        return self.success(ProblemAdminSerializer(problem).data)

    @validate_serializer(EditAssignmentProblemSerializer)
    @admin_role_required
    def put(self, request):
        data = request.data
        user = request.user

        problem_id = data.pop("id")
        assignment_id = Problem.objects.get(id=problem_id).assignment_id
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            ensure_created_by(assignment, user)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")

        try:
            problem = Problem.objects.get(id=problem_id, assignment=assignment)
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")

        _id = data["_id"]
        if not _id:
            return self.error("Display ID is required")
        if Problem.objects.exclude(id=problem_id).filter(_id=_id, assignment=assignment).exists():
            return self.error("Display ID already exists")

        error_info = self.common_checks(request)
        if error_info:
            return self.error(error_info)

        tags = data.pop("tags")
        data["languages"] = list(data["languages"])

        for k, v in data.items():
            setattr(problem, k, v)
        problem.save()

        problem.tags.remove(*problem.tags.all())
        for tag in tags:
            try:
                tag = ProblemTag.objects.get(name=tag)
            except ProblemTag.DoesNotExist:
                tag = ProblemTag.objects.create(name=tag)
            problem.tags.add(tag)
        return self.success(ProblemAdminSerializer(problem).data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem.",
                required=True
            ),
        ],
        operation_description="Delete certain problem of assignment."
    )
    @admin_role_required
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            problem = Problem.objects.get(id=id, assignment_id__isnull=False)
            ensure_created_by(problem.assignment, request.user)
        except Problem.DoesNotExist:
            return self.error("Problem does not exists")

        if Submission.objects.filter(problem=problem).exists():
            return self.error("Can't delete the problem as it has submissions")

        problem.delete()
        return self.success()


class AddAssignmentProblemAPI(APIView):
    @validate_serializer(AddAssignmentProblemSerializer)
    @swagger_auto_schema(
        request_body=AddAssignmentProblemSerializer,
        operation_description="Add problems from public problems into the assignment."
    )
    def post(self, request):
        data = request.data
        try:
            assignment = Assignment.objects.get(id=data["assignment_id"])
            ensure_created_by(assignment, request.user)
            problem = Problem.objects.get(id=data["problem_id"])
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")

        if assignment.status == AssignmentStatus.ASSIGNMENT_ENDED:
            return self.error("Assignment deadline has expired")
        if Problem.objects.filter(assignment=assignment, _id=data["display_id"]).exists():
            return self.error("Duplicate display id in this assignment")

        total_score = 0
        for item in problem.test_case_score:
            total_score += item["score"]
        problem.total_score = total_score
        tags = problem.tags.all()
        problem.pk = None
        problem.assignment = assignment
        problem.rule_type = ProblemRuleType.ASSIGNMENT
        problem.is_public = True
        problem.visible = True
        problem._id = request.data["display_id"]
        problem.submission_number = problem.accepted_number = 0
        problem.statistic_info = {}
        problem.save()
        problem.tags.set(tags)
        return self.success()
