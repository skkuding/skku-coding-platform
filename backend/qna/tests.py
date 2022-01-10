from copy import deepcopy
from utils.api.tests import APITestCase
from course.models import Course
from .models import Question, Answer


DEFAULT_COURSE_DATA = { "title": "Test",
                        "course_code": "TESTCODE12",
                        "class_number": 43,
                        "registered_year": 2021,
                        "semester": 1 }

DEFAULT_QUESTION_DATA = { "title": "title",
                          "content": "content",
                          "status": True }


class QuestionAPITest(APITestCase):
    pass


class AnswerAPITest(APITestCase):
    def setUp(self):
        self.user = self.create_user("2020300000", "pass")
        self.url = self.reverse("answer_api")
        self.question_id = self.create_question()
        
        self.data = { "question_id": self.question_id,
                      "created_by_id": self.user.id,
                      "content": "content",
                      "closure": False }

    def create_question(self):
        self.professor = self.create_admin(login=False)
        course_id = Course.objects.create(created_by=self.professor, **DEFAULT_COURSE_DATA).id
        return Question.objects.create(created_by_id=self.user.id, course_id=course_id, title="title", content="content", status=True).id
    
    def test_create_answer(self):
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        return response.data["data"]["id"]
    
    def test_edit_answer(self):
        id = self.test_create_answer()
        self.data.update({"id":id, "content":"update content"})
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
        self.data.update({"closure":True})
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        self.assertFalse(Question.objects.get(id=self.question_id).status)

    def test_unauthorized_closure(self):
        self.create_user("2020700000", "pass")
        self.data.update({"closure":True})
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
        self.client.put(self.reverse("user_profile_api"), data={"real_name":"Jane Doe"})

        self.data.update({"created_by_id":self.professor.id})
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data["data"]["admin_type"], "Professor")
        self.assertEqual(response.data["data"]["name"], "Jane Doe")
    
    def test_student_answer(self):
        student = self.create_user("2020700000", "pass")
        self.data.update({"created_by_id":student.id})
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data["data"]["admin_type"], "None")
        self.assertEqual(response.data["data"]["name"], "2020700000")