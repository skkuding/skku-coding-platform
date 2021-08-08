from utils.api import validate_serializer
from account.decorators import ensure_created_by

from submission.models import Submission
from assignment.models import Assignment
from .admin import ProblemBase

from ..models import Problem, ProblemTag
from ..serializers import (CreateAssignmentProblemSerializer, ProblemAdminSerializer, 
                            ProblemProfessorSerializer, EditAssignmentProblemSerializer)


class AssignmentProblemAPI(ProblemBase):
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

        problems = Problem.objects.filter(assignment=assignment).order_by("-create_time")
        return self.success(self.paginate_data(request, problems, ProblemProfessorSerializer))
    
    @validate_serializer(CreateAssignmentProblemSerializer)
    def post(self, request):
        data = request.data
        try:
            assignment = Assignment.objects.get(id=data.pop("assignment_id"))
            ensure_created_by(assignment, request.user)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")

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
    def put(self, request):
        data = request.data
        user = request.user

        try:
            assignment = Assignment.objects.get(id=data.pop("assignment_id"))
            ensure_created_by(assignment, user)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")

        problem_id = data.pop("id")

        try:
            problem = Problem.objects.get(id=problem_id, assignment=assignment)
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")

        _id = data["_id"]
        if not _id:
            return self.error("Display ID is required")
        if Problem.objects.exclude(id=problem_id).filter(_id=_id, contest=assignment).exists():
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
        return self.success()

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