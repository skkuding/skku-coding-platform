import copy
from utils.api.tests import APITestCase
from .models import Question, Answer
from course.models import Course
from django.utils import timezone


DEFAULT_COURSE_DATA = {"title": "test course",
                       "course_code": "ABCD123",
                       "class_number": 12,
                       "registered_year": 2021,
                       "semester": 1}

DEFAULT_QUESTION_DATA = {"title": "title",
                         "content": "content",
                         "create_time": timezone.localtime(timezone.now()),
                         "last_update_time": timezone.localtime(timezone.now())}


class QuestionAPITest(APITestCase):
    def setUp(self):
        professor = self.create_admin()
        self.course_id = Course.objects.create(created_by=professor, **DEFAULT_COURSE_DATA).id
        self.data = copy.deepcopy(DEFAULT_QUESTION_DATA)
        self.data["course_id"] = self.course_id
        self.url = self.reverse("question_api")

    def test_create_question(self):
        res = self.client.post(self.url, data=self.data)
        self.assertSuccess(res)
        return res

    def test_edit_question(self):
        id = self.test_create_question().data["data"]["id"]
        update_data = {"id": id,
                       "title": "update title",
                       "content": "update content"}
        data = copy.deepcopy(self.data)
        data.update(update_data)
        res = self.client.put(self.url, data=update_data)
        self.assertSuccess(res)
        res_data = res.data["data"]
        self.assertEqual(res_data["title"], "update title")
        self.assertEqual(res_data["content"], "update content")

    def test_get_question_list(self):
        self.test_create_question()
        response = self.client.get(f"{self.url}?course_id={self.course_id}")
        self.assertSuccess(response)

    def test_get_one_question(self):
        id = self.test_create_question().data["data"]["id"]
        response = self.client.get(f"{self.url}?course_id={self.course_id}&question_id={id}")
        self.assertSuccess(response)

    def test_delete_question(self):
        id = self.test_create_question().data["data"]["id"]
        res = self.client.delete(f"{self.url}?course_id={self.course_id}&question_id={id}")
        self.assertSuccess(res)
        self.assertFalse(Question.objects.filter(id=id).exists())


class QuestionProfessorAPITest(APITestCase):
    def setUp(self):
        professor = self.create_admin()
        self.course_id = Course.objects.create(created_by=professor, **DEFAULT_COURSE_DATA).id
        self.data = copy.deepcopy(DEFAULT_QUESTION_DATA)
        self.data["course_id"] = self.course_id
        self.question_id = Question.objects.create(created_by=professor, **self.data).id
        self.url = self.reverse("question_professor_api")

    def test_get_assignment_list(self):
        resp = self.client.get(f"{self.url}?course_id={self.course_id}")
        self.assertSuccess(resp)

    def test_get_one_assignment(self):
        resp = self.client.get(f"{self.url}?course_id={self.course_id}&question_id={self.question_id}")
        self.assertSuccess(resp)


class AnswerAPITest(APITestCase):
    def setUp(self):
        self.user = self.create_user("2020300000", "pass")
        self.url = self.reverse("answer_api")
        self.question_id = self.create_question()

        self.data = {"question_id": self.question_id,
                     "created_by_id": self.user.id,
                     "content": "content",
                     "closure": False}

    def create_question(self):
        self.professor = self.create_admin(login=False)
        course_id = Course.objects.create(created_by=self.professor, **DEFAULT_COURSE_DATA).id
        return Question.objects.create(created_by_id=self.user.id, course_id=course_id, title="title", content="content").id

    def test_create_answer(self):
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        return response.data["data"]["id"]

    def test_edit_answer(self):
        id = self.test_create_answer()
        self.data.update({"id": id, "content": "update content"})
        response = self.client.put(self.url, data=self.data)
        self.assertSuccess(response)
        response_data = response.data["data"]["content"]
        self.assertEqual(response_data, "update content")

    def test_list_answer(self):
        self.test_create_answer()
        response = self.client.get(f"{self.url}?question_id={self.question_id}")
        self.assertSuccess(response)

    def test_delete_answer(self):
        id = self.test_create_answer()
        response = self.client.delete(f"{self.url}?id={id}")
        self.assertSuccess(response)
        self.assertFalse(Answer.objects.filter(id=id).exists())

    def test_question_closure(self):
        self.data.update({"closure": True})
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        self.assertFalse(Question.objects.get(id=self.question_id).is_open)

    def test_unauthorized_closure(self):
        self.create_user("2020700000", "pass")
        self.data.update({"closure": True})
        response = self.client.post(self.url, data=self.data)
        self.assertFailed(response, "No permission for closure")

    def test_unauthorized_action(self):
        id = self.test_create_answer()
        self.client.login(username="admin", password="admin")
        response = self.client.delete(f"{self.url}?id={id}")
        self.assertFailed(response, "No permission for this action")

    def test_creator_answer(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data["data"]["admin_type"], "Creator")
        self.assertEqual(response.data["data"]["name"], "2020300000")

    def test_professor_answer(self):
        self.client.login(username="admin", password="admin")
        self.client.put(self.reverse("user_profile_api"), data={"real_name": "Jane Doe"})

        self.data.update({"created_by_id": self.professor.id})
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data["data"]["admin_type"], "Professor")
        self.assertEqual(response.data["data"]["name"], "Jane Doe")

    def test_student_answer(self):
        student = self.create_user("2020700000", "pass")
        self.data.update({"created_by_id": student.id})
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data["data"]["admin_type"], "None")
        self.assertEqual(response.data["data"]["name"], "2020700000")
