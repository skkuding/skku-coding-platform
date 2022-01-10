import copy
from utils.api.tests import APITestCase
from .models import Question, Answer
from course.models import Course
from django.utils import timezone

#contest test 참조하기
DEFAULT_COURSE_DATA = {"title": "test course",
                       "course_code": "ABCD123",
                       "class_number": 12,
                       "registered_year": 2021,
                       "semester": 1}

DEFAULT_QUESTION_DATA = {"title" : "Test", "content" : "TestTest",
                         "create_time" : timezone.localtime(timezone.now()),
                         "last_update_time" : timezone.localtime(timezone.now())}

class QuestionAPITest(APITestCase):
    def setUp(self):
        professor = self.create_admin()
        self.course_id = Course.objects.create(created_by=professor, **DEFAULT_COURSE_DATA).id
        # student_id = student.id
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
                       "content" : "update content"}
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

    def test_delete_question(self):
        id = self.test_create_question().data["data"]["id"]
        res = self.client.delete(f"{self.url}?course_id={self.course_id}&question_id={id}")
        self.assertSuccess(res)
        self.assertFalse(Question.objects.filter(id=id).exists())

class AnswerAPITest(APITestCase):
    def setUp(self):
        #question 만들기가 선행되어야 해서 아직 작성하지 않았습니다!
        pass
    
    def test_create_answer(self):
        pass
    
    def test_edit_answer(self):
        pass

    def test_list_answer(self):
        pass

    def test_delete_answer(self):
        pass