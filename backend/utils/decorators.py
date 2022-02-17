import functools
import hashlib
import time

from assignment.models import Assignment
from group.models import Group, GroupMember
from problem.models import Problem
from course.models import Registration
from contest.models import Contest, ContestType, ContestStatus, ContestRuleType
from .api import JSONResponse, APIError
from .constants import CONTEST_PASSWORD_SESSION_KEY, AssignmentStatus
from account.models import ProblemPermission


class BasePermissionDecorator(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type):
        return functools.partial(self.__call__, obj)

    def error(self, data):
        return JSONResponse.response({"error": "permission-denied", "data": data})

    def __call__(self, *args, **kwargs):
        self.request = args[1]

        if self.check_permission():
            if self.request.user.is_disabled:
                return self.error("Your account is disabled")
            return self.func(*args, **kwargs)
        else:
            return self.error("Please login first")

    def check_permission(self):
        raise NotImplementedError()


class login_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated


class super_admin_required(BasePermissionDecorator):
    def check_permission(self):
        user = self.request.user
        return user.is_authenticated and user.is_super_admin()


class admin_role_required(BasePermissionDecorator):
    def check_permission(self):
        user = self.request.user
        return user.is_authenticated and user.is_admin_role()


class problem_permission_required(admin_role_required):
    def check_permission(self):
        if not super(problem_permission_required, self).check_permission():
            return False
        if self.request.user.problem_permission == ProblemPermission.NONE:
            return False
        return True


def check_contest_password(password, contest_password):
    if not (password and contest_password):
        return False
    if password == contest_password:
        return True
    else:
        # sig#timestamp
        # This form of password is also possible,
        # but no support is provided on the interface
        # sig = sha256(contest_password + timestamp)[:8]
        if "#" in password:
            s = password.split("#")
            if len(s) != 2:
                return False
            sig, ts = s[0], s[1]

            if sig == hashlib.sha256((contest_password + ts).encode("utf-8")).hexdigest()[:8]:
                try:
                    ts = int(ts)
                except Exception:
                    return False
                return int(time.time()) < ts
            else:
                return False
        else:
            return False


def check_contest_permission(check_type="details"):
    """
    Only for Class based view to check whether the user has the right
    to enter the contest, check_type optional details, problems, ranks, submissions
    If the verification is passed, the contest can be obtained through self.contest in the view
    """

    def decorator(func):
        def _check_permission(*args, **kwargs):
            self = args[0]
            request = args[1]
            user = request.user
            if request.data.get("contest_id"):
                contest_id = request.data["contest_id"]
            else:
                contest_id = request.GET.get("contest_id")
            if not contest_id:
                return self.error("Parameter error, contest_id is required")

            try:
                # use self.contest to avoid query contest again in view.
                self.contest = Contest.objects.select_related("created_by").get(id=contest_id, visible=True)
            except Contest.DoesNotExist:
                return self.error("Contest %s doesn't exist" % contest_id)

            # Anonymous
            if not user.is_authenticated:
                return self.error("Please login first.")

            # creator or owner
            if user.is_contest_admin(self.contest):
                return func(*args, **kwargs)

            if self.contest.contest_type == ContestType.PASSWORD_PROTECTED_CONTEST:
                # password error
                if not check_contest_password(request.session.get(CONTEST_PASSWORD_SESSION_KEY, {}).get(self.contest.id), self.contest.password):
                    return self.error("Wrong password or password expired")

            # regular user get contest problems, ranks etc. before contest started
            if self.contest.status == ContestStatus.CONTEST_NOT_START and check_type != "details":
                return self.error("Contest has not started yet.")

            # allowed_groups exist and member doesn't belong to any group, error
            if self.contest.allowed_groups.count() and not self.contest.allowed_groups.filter(members=user).exists():
                if check_type == "ranks" or check_type == "submissions" or check_type == "problems":
                    return self.error("You are not a member of the group allowed to this contest")

            # check does user have permission to get ranks, submissions in OI Contest
            if self.contest.status == ContestStatus.CONTEST_UNDERWAY and self.contest.rule_type == ContestRuleType.OI:
                if not self.contest.real_time_rank and (check_type == "ranks" or check_type == "submissions"):
                    return self.error(f"No permission to get {check_type}")

            return func(*args, **kwargs)
        return _check_permission
    return decorator


def check_assignment_permission():
    def decorator(func):
        def _check_permission(*args, **kwargs):
            self = args[0]
            request = args[1]
            user = request.user
            if request.data.get("assignment_id"):
                assignment_id = request.data["assignment_id"]
            else:
                assignment_id = request.GET.get("assignment_id")
            if not assignment_id:
                return self.error("Parameter error, assignment_id is required")

            try:
                self.assignment = Assignment.objects.select_related("created_by").get(id=assignment_id, visible=True)
            except Assignment.DoesNotExist:
                return self.error("Assignment %s doesn't exist" % assignment_id)

            if not user.is_authenticated:
                return self.error("Please login first.")

            if user.is_assignment_admin(self.assignment):
                return func(*args, **kwargs)

            if self.assignment.status == AssignmentStatus.ASSIGNMENT_NOT_START:
                return self.error("Assignment has not started yet.")

            # check if user is registered to the course
            try:
                Registration.objects.get(user_id=user.id, course_id=self.assignment.course_id)
            except Registration.DoesNotExist:
                return self.error("Invalid access, not registered user")

            return func(*args, **kwargs)
        return _check_permission
    return decorator


def check_group_admin():
    def decorator(func):
        def _check_permission(*args, **kwargs):
            self = args[0]
            request = args[1]
            user = request.user

            if not user.is_authenticated:
                return self.error("Please login first.")

            group_id = request.data["group_id"] if request.data.get("group_id") else request.GET.get("group_id")
            if not group_id:
                return self.error("Parameter error, group_id is required")

            if not Group.objects.filter(id=group_id).exists():
                return self.error("Group does not exist")
            if not GroupMember.objects.filter(group=group_id, user=user, is_group_admin=True).exists():
                return self.error("permission-denied: Group admin is required")

            return func(*args, **kwargs)
        return _check_permission
    return decorator


def ensure_created_by(obj, user):
    e = APIError(msg=f"{obj.__class__.__name__} does not exist")
    if not user.is_admin_role():
        raise e
    if user.is_super_admin():
        return
    if isinstance(obj, Problem):
        if not user.can_mgmt_all_problem() and obj.created_by != user:
            raise e
    elif obj.created_by != user:
        raise e
