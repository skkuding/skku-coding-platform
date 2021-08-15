from copy import deepcopy
from unittest import mock

from problem.models import Problem, ProblemTag
from problem.tests import DEFAULT_PROBLEM_DATA
from course.models import Course, Registration
from course.tests import DEFAULT_COURSE_DATA
from assignment.models import Assignment
from assignment.tests import DEFAULT_ASSIGNMENT_DATA
from utils.api.tests import APITestCase
from .models import Submission


DEFAULT_SUBMISSION_DATA = {
    "problem_id": "1",
    "user_id": 1,
    "username": "test",
    "code": "xxxxxxxxxxxxxx",
    "result": -2,
    "info": {},
    "language": "C",
    "statistic_info": {"score": 0, "err_info": "test"}
}


# todo contest submission


class SubmissionPrepare(APITestCase):
    def _create_problem_and_submission(self):
        user = self.create_admin("test", "test123", login=False)
        problem_data = deepcopy(DEFAULT_PROBLEM_DATA)
        tags = problem_data.pop("tags")
        problem_data["created_by"] = user
        self.problem = Problem.objects.create(**problem_data)
        for tag in tags:
            tag = ProblemTag.objects.create(name=tag)
            self.problem.tags.add(tag)
        self.problem.save()
        self.submission_data = deepcopy(DEFAULT_SUBMISSION_DATA)
        self.submission_data["problem_id"] = self.problem.id
        self.submission = Submission.objects.create(**self.submission_data)

    def _create_assignment_submission(self):
        professor = self.create_admin()
        self.course_id = Course.objects.create(created_by=professor, **DEFAULT_COURSE_DATA).id
        assignment_data = deepcopy(DEFAULT_ASSIGNMENT_DATA)
        assignment_data["course_id"] = self.course_id
        self.assignment_id = Assignment.objects.create(created_by=professor, **assignment_data).id
        self.problem_data = deepcopy(DEFAULT_PROBLEM_DATA)
        self.problem_data["assignment_id"] = self.assignment_id
        self.problem = self.client.post(self.reverse("assignment_problem_professor_api"), data=self.problem_data).data["data"]
        self.submission_data = deepcopy(DEFAULT_SUBMISSION_DATA)
        self.submission_data["problem_id"] = self.problem["id"]
        self.submission_data["assignment_id"] = self.assignment_id
        self.submission = Submission.objects.create(**self.submission_data)


class SubmissionListTest(SubmissionPrepare):
    def setUp(self):
        self._create_problem_and_submission()
        self.create_user("123", "345")
        self.url = self.reverse("submission_list_api")

    def test_get_submission_list(self):
        resp = self.client.get(self.url, data={"limit": "10"})
        self.assertSuccess(resp)


@mock.patch("judge.tasks.judge_task.send")
class SubmissionAPITest(SubmissionPrepare):
    def setUp(self):
        self.url = self.reverse("submission_api")

    def test_create_submission(self, judge_task):
        self._create_problem_and_submission()
        self.create_user("123", "test123")
        resp = self.client.post(self.url, self.submission_data)
        self.assertSuccess(resp)
        judge_task.assert_called()

    def test_create_assignment_submission(self, judge_task):
        self._create_assignment_submission()
        student = self.create_user("123", "test123")
        Registration.objects.create(user_id=student.id, course_id=self.course_id)
        resp = self.client.post(self.url, self.submission_data)
        self.assertSuccess(resp)
        judge_task.assert_called()

    def test_create_submission_with_wrong_language(self, judge_task):
        self._create_problem_and_submission()
        self.create_user("123", "test123")
        self.submission_data.update({"language": "Python3"})
        resp = self.client.post(self.url, self.submission_data)
        self.assertFailed(resp)
        self.assertDictEqual(resp.data, {"error": "error",
                                         "data": "Python3 is now allowed in the problem"})
        judge_task.assert_not_called()


class AssignmentSubmissionListTest(SubmissionPrepare):
    def setUp(self):
        self._create_assignment_submission()
        self.url = self.reverse("assignment_submission_list_api")

    def test_get_assignment_submission_list(self):
        problem_id = self.problem["_id"]
        resp = self.client.get(f"{self.url}?assignment_id={self.assignment_id}&problem_id={problem_id}")
        self.assertSuccess(resp)

    def test_get_student_assignment_submission_list(self):
        student = self.create_user("2020123123", "123")
        Registration.objects.create(user_id=student.id, course_id=self.course_id)
        self.submission_data["user_id"] = student.id
        self.submission_data["username"] = student.username
        Submission.objects.create(**self.submission_data)
        problem_id = self.problem["_id"]
        resp = self.client.get(f"{self.url}?assignment_id={self.assignment_id}&problem_id={problem_id}")
        self.assertSuccess(resp)


class AssignmentSubmissionListProfessorTest(SubmissionPrepare):
    def setUp(self):
        self._create_assignment_submission()
        self.url = self.reverse("assignment_submission_list_professor_api")

    def test_get_assignment_submission_list_professor(self):
        assignment_id = self.assignment_id
        problem_id = self.problem["id"]
        resp = self.client.get(f"{self.url}?assignment_id={assignment_id}&problem_id={problem_id}")
        self.assertSuccess(resp)


class EditSubmissionScoreTest(SubmissionPrepare):
    def setUp(self):
        self._create_assignment_submission()
        self.url = self.reverse("edit_submission_score_api")

    def test_edit_submission_score(self):
        submission_id = self.submission.id
        data = {"id": submission_id, "score": 100}
        resp = self.client.put(self.url, data=data)
        self.assertSuccess(resp)
        resp_data = resp.data["data"]
        self.assertEqual(resp_data["statistic_info"]["score"], 100)
