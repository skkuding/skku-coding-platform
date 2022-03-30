import hashlib
import json
import os
import zipfile
from wsgiref.util import FileWrapper

from django.conf import settings
from django.db.models import Q
from django.http import StreamingHttpResponse

from contest.models import Contest, ContestStatus
from judge.dispatcher import SPJCompiler
from submission.models import Submission
from utils.api import APIView, CSRFExemptAPIView, validate_serializer, APIError
from utils.decorators import problem_permission_required, ensure_created_by
from utils.shortcuts import rand_str, natural_sort_key
from ..models import Problem, ProblemRuleType, ProblemSetGroup, ProblemTag, ProblemSet
from ..serializers import (CreateContestProblemSerializer, CompileSPJSerializer, CreateProblemSetGroupSerializer, CreateProblemSetSerializer,
                           EditProblemSetGroupSerializer, EditProblemSetSerializer, CreateProblemSerializer, EditProblemSerializer, EditContestProblemSerializer,
                           ProblemAdminSerializer, ProblemSetGroupSerializer, ProblemSetSerializer, TestCaseUploadForm, ContestProblemMakePublicSerializer,
                           AddContestProblemSerializer, TestCaseTextSerializer)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser


class TestCaseZipProcessor(object):
    def process_zip(self, uploaded_zip_file, spj, dir=""):
        try:
            zip_file = zipfile.ZipFile(uploaded_zip_file, "r")
        except zipfile.BadZipFile:
            raise APIError("Bad zip file")
        name_list = zip_file.namelist()
        test_case_list = self.filter_name_list(name_list, spj=spj, dir=dir)
        if not test_case_list:
            raise APIError("Empty file")

        test_case_id = rand_str()
        test_case_dir = os.path.join(settings.TEST_CASE_DIR, test_case_id)
        os.mkdir(test_case_dir)
        os.chmod(test_case_dir, 0o710)

        size_cache = {}
        md5_cache = {}

        for item in test_case_list:
            with open(os.path.join(test_case_dir, item), "wb") as f:
                content = zip_file.read(f"{dir}{item}").replace(b"\r\n", b"\n")
                size_cache[item] = len(content)
                if item.endswith(".out"):
                    md5_cache[item] = hashlib.md5(content.rstrip()).hexdigest()
                f.write(content)
        test_case_info = {"spj": spj, "test_cases": {}}

        info = []

        if spj:
            for index, item in enumerate(test_case_list):
                data = {"input_name": item, "input_size": size_cache[item]}
                info.append(data)
                test_case_info["test_cases"][str(index + 1)] = data
        else:
            # ["1.in", "1.out", "2.in", "2.out"] => [("1.in", "1.out"), ("2.in", "2.out")]
            test_case_list = zip(*[test_case_list[i::2] for i in range(2)])
            for index, item in enumerate(test_case_list):
                data = {"stripped_output_md5": md5_cache[item[1]],
                        "input_size": size_cache[item[0]],
                        "output_size": size_cache[item[1]],
                        "input_name": item[0],
                        "output_name": item[1]}
                info.append(data)
                test_case_info["test_cases"][str(index + 1)] = data

        with open(os.path.join(test_case_dir, "info"), "w", encoding="utf-8") as f:
            f.write(json.dumps(test_case_info, indent=4))

        for item in os.listdir(test_case_dir):
            os.chmod(os.path.join(test_case_dir, item), 0o640)

        return info, test_case_id

    def filter_name_list(self, name_list, spj, dir=""):
        ret = []
        prefix = 1
        if spj:
            while True:
                in_name = f"{prefix}.in"
                if f"{dir}{in_name}" in name_list:
                    ret.append(in_name)
                    prefix += 1
                    continue
                else:
                    return sorted(ret, key=natural_sort_key)
        else:
            while True:
                in_name = f"{prefix}.in"
                out_name = f"{prefix}.out"
                if f"{dir}{in_name}" in name_list and f"{dir}{out_name}" in name_list:
                    ret.append(in_name)
                    ret.append(out_name)
                    prefix += 1
                    continue
                else:
                    return sorted(ret, key=natural_sort_key)


class TestCaseAPI(CSRFExemptAPIView, TestCaseZipProcessor):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="problem_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem that you want to get test cases",
                required=True
            )
        ],
        operation_description="Get testcase of certain problem."
    )
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if not problem_id:
            return self.error("Parameter error, problem_id is required")
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return self.error("Problem does not exists")

        if problem.contest:
            ensure_created_by(problem.contest, request.user)
        else:
            ensure_created_by(problem, request.user)

        test_case_dir = os.path.join(settings.TEST_CASE_DIR, problem.test_case_id)
        if not os.path.isdir(test_case_dir):
            return self.error("Test case does not exists")
        name_list = self.filter_name_list(os.listdir(test_case_dir), problem.spj)
        name_list.append("info")
        file_name = os.path.join(test_case_dir, problem.test_case_id + ".zip")
        with zipfile.ZipFile(file_name, "w") as file:
            for test_case in name_list:
                file.write(f"{test_case_dir}/{test_case}", test_case)
        response = StreamingHttpResponse(FileWrapper(open(file_name, "rb")),
                                         content_type="application/octet-stream")

        response["Content-Disposition"] = f"attachment; filename=problem_{problem.id}_test_cases.zip"
        response["Content-Length"] = os.path.getsize(file_name)
        return response

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="spj", in_=openapi.IN_FORM, type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="file", in_=openapi.IN_FORM, type=openapi.TYPE_FILE
            )
        ],
        operation_description="Upload testcases. Returned \'id\' would be used when uploading problems(for \'testcase_id\')"
    )
    def post(self, request):
        form = TestCaseUploadForm(request.POST, request.FILES)
        if form.is_valid():
            spj = form.cleaned_data["spj"] == "true"
            file = form.cleaned_data["file"]
        else:
            return self.error("Upload failed")
        zip_file = f"/tmp/{rand_str()}.zip"
        with open(zip_file, "wb") as f:
            for chunk in file:
                f.write(chunk)
        info, test_case_id = self.process_zip(zip_file, spj=spj)
        os.remove(zip_file)
        return self.success({"id": test_case_id, "info": info, "spj": spj})


class TestCaseTextAPI(CSRFExemptAPIView, TestCaseZipProcessor):
    @swagger_auto_schema(
        request_body=TestCaseTextSerializer,
        operation_description="Upload testcases. Returned \'id\' would be used when uploading problems(for \'testcase_id\')"
    )
    def post(self, request):
        data = request.data
        spj = data["spj"]
        testcases = data["testcases"]

        if not testcases:
            return self.error("Testcase is required")

        test_case_id = rand_str()
        test_case_dir = os.path.join(settings.TEST_CASE_DIR, test_case_id)
        os.mkdir(test_case_dir, mode=0o710)

        try:
            for i, testcase in enumerate(testcases):
                in_path = os.path.join(test_case_dir, f"{i+1}.in")
                with open(in_path, "w") as f:
                    f.write(testcase["input"])

                out_path = os.path.join(test_case_dir, f"{i+1}.out")
                with open(out_path, "w") as f:
                    f.write(testcase["output"])
        except KeyError:
            return self.error("input or output file does not exist.")

        test_case_info = {"spj": spj, "test_cases": {}}

        info = []

        if spj:
            for i, testcase in enumerate(testcases):
                data = {"input_name": f"{i+1}.in", "input_size": len(testcase["input"])}
                info.append(data)
                test_case_info["test_cases"][str(i + 1)] = data
        else:
            for i, testcase in enumerate(testcases):
                data = {"stripped_output_md5": hashlib.md5(testcase["output"].rstrip().encode("utf-8")).hexdigest(),
                        "input_size": len(testcase["input"]),
                        "output_size": len(testcase["output"]),
                        "input_name": f"{i+1}.in",
                        "output_name": f"{i+1}.out"}
                info.append(data)
                test_case_info["test_cases"][str(i + 1)] = data

        with open(os.path.join(test_case_dir, "info"), "w", encoding="utf-8") as f:
            f.write(json.dumps(test_case_info, indent=4))

        for item in os.listdir(test_case_dir):
            os.chmod(os.path.join(test_case_dir, item), 0o640)

        return self.success({"id": test_case_id, "info": info, "spj": spj})

    def get(self, request):
        problem_id = request.GET.get("id")
        if not problem_id:
            return self.error("Parameter error, problem_id is required")
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return self.error("Problem does not exists")

        if problem.contest:
            ensure_created_by(problem.contest, request.user)
        elif problem.assignment:
            ensure_created_by(problem.assignment, request.user)
        else:
            ensure_created_by(problem, request.user)

        test_case_dir = os.path.join(settings.TEST_CASE_DIR, problem.test_case_id)
        if not os.path.isdir(test_case_dir):
            return self.error("Test case does not exists")

        name_list = self.filter_name_list(os.listdir(test_case_dir), problem.spj)
        testcases = {"testcases": [], "spj": problem.spj}

        if not problem.spj:
            for i in range(0, len(name_list), 2):
                testcase = {}
                with open(os.path.join(test_case_dir, name_list[i]), "r") as f:
                    testcase["input"] = f.read()
                with open(os.path.join(test_case_dir, name_list[i + 1]), "r") as f:
                    testcase["output"] = f.read()
                testcases["testcases"].append(testcase)
        else:
            for i in range(len(name_list)):
                testcase = {}
                with open(os.path.join(test_case_dir, name_list[i]), "r") as f:
                    testcase["input"] = f.read()
                testcases["testcases"].append(testcase)

        return self.success(TestCaseTextSerializer(testcases).data)


class CompileSPJAPI(APIView):
    @validate_serializer(CompileSPJSerializer)
    @swagger_auto_schema(
        request_body=(CompileSPJSerializer),
        operation_description="Post code for special judge."
    )
    def post(self, request):
        data = request.data
        spj_version = rand_str(8)
        error = SPJCompiler(data["spj_code"], spj_version, data["spj_language"]).compile_spj()
        if error:
            return self.error(error)
        else:
            return self.success()


class ProblemBase(APIView):
    def common_checks(self, request):
        data = request.data
        if data["spj"]:
            if not data["spj_language"] or not data["spj_code"]:
                return "Invalid spj"
            if not data["spj_compile_ok"]:
                return "SPJ code must be compiled successfully"
            data["spj_version"] = hashlib.md5(
                (data["spj_language"] + ":" + data["spj_code"]).encode("utf-8")).hexdigest()
        else:
            data["spj_language"] = None
            data["spj_code"] = None
        if data["rule_type"] in (ProblemRuleType.OI, ProblemRuleType.ASSIGNMENT):
            total_score = 0
            for item in data["test_case_score"]:
                if item["score"] <= 0:
                    return "Invalid score"
                else:
                    total_score += item["score"]
            data["total_score"] = total_score
        data["languages"] = list(data["languages"])


class ProblemAPI(ProblemBase):
    @problem_permission_required
    @validate_serializer(CreateProblemSerializer)
    @swagger_auto_schema(
        request_body=CreateProblemSerializer,
        operation_description="Uploading problem."
    )
    def post(self, request):
        data = request.data
        _id = data["_id"]
        if Problem.objects.filter(_id=_id, contest_id__isnull=True, assignment_id__isnull=True).exists():
            return self.error("Display ID already exists")

        error_info = self.common_checks(request)
        if error_info:
            return self.error(error_info)

        # todo check filename and score info
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

    @problem_permission_required
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem. ",
            ),
            openapi.Parameter(
                name="rule_type", in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Rule type of problem: ACM or OI",
            ),
            openapi.Parameter(
                name="keyword", in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="keyword of problem\'s title you want to search with",
            ),
        ],
        operation_description="Get problem list"
    )
    def get(self, request):
        problem_id = request.GET.get("id")
        rule_type = request.GET.get("rule_type")
        user = request.user
        if problem_id:
            try:
                problem = Problem.objects.get(id=problem_id)
                ensure_created_by(problem, request.user)
                return self.success(ProblemAdminSerializer(problem).data)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        problems = Problem.objects.filter(contest_id__isnull=True, assignment_id__isnull=True).order_by("-create_time")
        if rule_type:
            if rule_type not in ProblemRuleType.choices():
                return self.error("Invalid rule_type")
            else:
                problems = problems.filter(rule_type=rule_type)

        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            problems = problems.filter(Q(title__icontains=keyword) | Q(_id__icontains=keyword))
        if not user.can_mgmt_all_problem():
            problems = problems.filter(created_by=user)
        return self.success(self.paginate_data(request, problems, ProblemAdminSerializer))

    @problem_permission_required
    @validate_serializer(EditProblemSerializer)
    @swagger_auto_schema(
        request_body=(EditProblemSerializer),
        operation_description="Editing problem."
    )
    def put(self, request):
        data = request.data
        problem_id = data.pop("id")

        try:
            problem = Problem.objects.get(id=problem_id)
            ensure_created_by(problem, request.user)
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")

        _id = data["_id"]
        if not _id:
            return self.error("Display ID is required")
        if Problem.objects.exclude(id=problem_id).filter(_id=_id, contest_id__isnull=True, assignment_id__isnull=True).exists():
            return self.error("Display ID already exists")

        error_info = self.common_checks(request)
        if error_info:
            return self.error(error_info)
        # todo check filename and score info
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

    @problem_permission_required
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem.",
                required=True
            ),
        ],
        operation_description="Delete certain problem."
    )
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            problem = Problem.objects.get(id=id, contest_id__isnull=True, assignment_id__isnull=True)
        except Problem.DoesNotExist:
            return self.error("Problem does not exists")
        ensure_created_by(problem, request.user)
        # d = os.path.join(settings.TEST_CASE_DIR, problem.test_case_id)
        # if os.path.isdir(d):
        #     shutil.rmtree(d, ignore_errors=True)
        problem.delete()
        return self.success()


class ContestProblemAPI(ProblemBase):
    @validate_serializer(CreateContestProblemSerializer)
    @swagger_auto_schema(
        request_body=(CreateContestProblemSerializer),
        operation_description="Create problems for contest."
    )
    def post(self, request):
        data = request.data
        try:
            contest = Contest.objects.get(id=data.pop("contest_id"))
            ensure_created_by(contest, request.user)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")

        if data["rule_type"] != contest.rule_type:
            return self.error("Invalid rule type")

        _id = data["_id"]

        if Problem.objects.filter(_id=_id, contest=contest).exists():
            return self.error("Duplicate Display id")

        error_info = self.common_checks(request)
        if error_info:
            return self.error(error_info)

        # todo check filename and score info
        data["contest"] = contest
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem.",
            ),
            openapi.Parameter(
                name="contest_id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of contest.",
                required=True
            ),
            openapi.Parameter(
                name="keyword", in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="keyword of problem\'s title you want to search with",
            ),
        ],
        operation_description="Get problems of certain contest. If problem_id is set, certain problem would be returned."
    )
    def get(self, request):
        problem_id = request.GET.get("id")
        contest_id = request.GET.get("contest_id")
        user = request.user
        if problem_id:
            try:
                problem = Problem.objects.get(id=problem_id)
                ensure_created_by(problem.contest, user)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")
            return self.success(ProblemAdminSerializer(problem).data)

        if not contest_id:
            return self.error("Contest id is required")
        try:
            contest = Contest.objects.get(id=contest_id)
            ensure_created_by(contest, user)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        problems = Problem.objects.filter(contest=contest).order_by("-create_time")
        if user.is_admin():
            problems = problems.filter(contest__created_by=user)
        keyword = request.GET.get("keyword")
        if keyword:
            problems = problems.filter(title__contains=keyword)
        return self.success(self.paginate_data(request, problems, ProblemAdminSerializer))

    @validate_serializer(EditContestProblemSerializer)
    @swagger_auto_schema(
        request_body=(EditContestProblemSerializer),
        operation_description="Edit problems of contest."
    )
    def put(self, request):
        data = request.data
        user = request.user

        try:
            contest = Contest.objects.get(id=data.pop("contest_id"))
            ensure_created_by(contest, user)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")

        if data["rule_type"] != contest.rule_type:
            return self.error("Invalid rule type")

        problem_id = data.pop("id")

        try:
            problem = Problem.objects.get(id=problem_id, contest=contest)
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")

        _id = data["_id"]
        if not _id:
            return self.error("Display ID is required")
        if Problem.objects.exclude(id=problem_id).filter(_id=_id, contest=contest).exists():
            return self.error("Display ID already exists")

        error_info = self.common_checks(request)
        if error_info:
            return self.error(error_info)
        # todo check filename and score info
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Unique id of problem.",
                required=True
            ),
        ],
        operation_description="Delete certain problem of contest."
    )
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")
        try:
            problem = Problem.objects.get(id=id, contest_id__isnull=False)
        except Problem.DoesNotExist:
            return self.error("Problem does not exists")
        ensure_created_by(problem.contest, request.user)
        if Submission.objects.filter(problem=problem).exists():
            return self.error("Can't delete the problem as it has submissions")
        # d = os.path.join(settings.TEST_CASE_DIR, problem.test_case_id)
        # if os.path.isdir(d):
        #    shutil.rmtree(d, ignore_errors=True)
        problem.delete()
        return self.success()


class ProblemLevelAPIView(APIView):
    def get(self, request):
        problemList = Problem.objects.filter(bank=True).values_list("difficulty", flat=True)
        counter = {}
        for level in problemList:
            counter[level] = counter.get(level, 0) + 1
        return self.success(counter)


class MakeContestProblemPublicAPIView(APIView):
    @validate_serializer(ContestProblemMakePublicSerializer)
    @problem_permission_required
    @swagger_auto_schema(
        request_body=(ContestProblemMakePublicSerializer),
        description="Make contest problems as public problems."
    )
    def post(self, request):
        data = request.data
        display_id = data.get("display_id")
        if Problem.objects.filter(_id=display_id, contest_id__isnull=True, assignment_id__isnull=True).exists():
            return self.error("Duplicate display ID")

        try:
            problem = Problem.objects.get(id=data["id"])
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")

        if not problem.contest or problem.is_public:
            return self.error("Already be a public problem")
        problem.is_public = True
        problem.save()
        # https://docs.djangoproject.com/en/1.11/topics/db/queries/#copying-model-instances
        tags = problem.tags.all()
        problem.pk = None
        problem.contest = None
        problem._id = display_id
        problem.visible = False
        problem.submission_number = problem.accepted_number = 0
        problem.statistic_info = {}
        problem.save()
        problem.tags.set(tags)
        return self.success()


class AddContestProblemAPI(APIView):
    @validate_serializer(AddContestProblemSerializer)
    @swagger_auto_schema(
        request_body=(AddContestProblemSerializer),
        operation_description="Add problems from public problems into the contest."
    )
    def post(self, request):
        data = request.data
        try:
            contest = Contest.objects.get(id=data["contest_id"])
            problem = Problem.objects.get(id=data["problem_id"])
        except (Contest.DoesNotExist, Problem.DoesNotExist):
            return self.error("Contest or Problem does not exist")

        if contest.status == ContestStatus.CONTEST_ENDED:
            return self.error("Contest has ended")
        if Problem.objects.filter(contest=contest, _id=data["display_id"]).exists():
            return self.error("Duplicate display id in this contest")

        tags = problem.tags.all()
        problem.pk = None
        problem.contest = contest
        problem.is_public = True
        problem.visible = True
        problem._id = request.data["display_id"]
        problem.submission_number = problem.accepted_number = 0
        problem.statistic_info = {}
        problem.save()
        problem.tags.set(tags)
        return self.success()


class ProblemSetGroupAPI(APIView):
    @validate_serializer(CreateProblemSetGroupSerializer)
    def post(self, request):
        data = request.data
        if ProblemSetGroup.objects.filter(title=data["title"]).exists():
            return self.error("Problem set group title already exists.")

        problem_set_group = ProblemSetGroup.objects.create(**data)

        return self.success(ProblemSetGroupSerializer(problem_set_group).data)

    @validate_serializer(EditProblemSetGroupSerializer)
    def put(self, request):
        data = request.data

        try:
            problem_set_group = ProblemSetGroup.objects.get(id=data.pop("id"))
        except ProblemSetGroup.DoesNotExist:
            return self.error("Problem set group does not exist.")

        for k, v in data.items():
            setattr(problem_set_group, k, v)
        problem_set_group.save()

        return self.success(ProblemSetGroupSerializer(problem_set_group).data)

    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")

        try:
            problem_set_group = ProblemSetGroup.objects.get(id=id)
        except ProblemSetGroup.DoesNotExist:
            return self.error("Problem set group does not exist.")

        problem_set_group.delete()
        return self.success()

    def get(self, request):
        id = request.GET.get("id")

        if not id:
            problem_set_group = ProblemSetGroup.objects.all()
            return self.success(ProblemSetGroupSerializer(problem_set_group, many=True).data)

        try:
            problem_set_group = ProblemSetGroup.objects.get(id=id)
            return self.success(ProblemSetGroupSerializer(problem_set_group).data)
        except ProblemSetGroup.DoesNotExist:
            return self.error("Problem set group does not exist.")


class ProblemSetAPI(APIView):
    @validate_serializer(CreateProblemSetSerializer)
    def post(self, request):
        data = request.data
        if ProblemSet.objects.filter(title=data["title"]).exists():
            return self.error("Problem set title already exists.")

        problem_set_group_id = data.pop("problem_set_group_id")
        try:
            problem_set_group = ProblemSetGroup.objects.get(id=problem_set_group_id)
        except ProblemSetGroup.DoesNotExist:
            return self.error("Problem set group does not exist.")

        data["problem_set_group"] = problem_set_group
        problem_set = ProblemSet.objects.create(**data)

        return self.success(ProblemSetSerializer(problem_set).data)

    @validate_serializer(EditProblemSetSerializer)
    def put(self, request):
        data = request.data

        try:
            problem_set = ProblemSet.objects.get(id=data.pop("id"))
        except ProblemSet.DoesNotExist:
            return self.error("Problem set does not exist.")

        problem_set_group_id = data.pop("problem_set_group_id")
        try:
            problem_set_group = ProblemSetGroup.objects.get(id=problem_set_group_id)
        except ProblemSetGroup.DoesNotExist:
            return self.error("Problem set group does not exist.")

        problem_ids = data.pop("problems")
        problems = Problem.objects.filter(id__in=problem_ids, assignment_id__isnull=True, contest_id__isnull=True)

        data["problem_set_group"] = problem_set_group
        for k, v in data.items():
            setattr(problem_set, k, v)
        problem_set.problems.set(problems)
        problem_set.save()

        return self.success(ProblemSetSerializer(problem_set).data)

    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid parameter, id is required")

        try:
            problem_set = ProblemSet.objects.get(id=id)
        except ProblemSet.DoesNotExist:
            return self.error("Problem set does not exist.")

        problem_set.delete()
        return self.success()

    def get(self, request):
        id = request.GET.get("id")
        problem_set_group_id = request.GET.get("problem_set_group_id")

        if not id:
            problem_set = ProblemSet.objects.filter(problem_set_group=problem_set_group_id)
            return self.success(ProblemSetSerializer(problem_set, many=True).data)

        try:
            problem_set = ProblemSet.objects.get(id=id)
            return self.success(ProblemSetSerializer(problem_set).data)
        except ProblemSet.DoesNotExist:
            return self.error("Problem set does not exist.")
