import copy
from datetime import timedelta
from django.utils import timezone

from utils.api.tests import APITestCase

from course.models import Registration, Course
from .models import Assignment

DEFAULT_COURSE_DATA = {"title": "test course",
                       "course_code": "ABCD123",
                       "class_number": 12,
                       "registered_year": 2021,
                       "semester": 1}

DEFAULT_ASSIGNMENT_DATA = {"title": "test assignment",
                           "content": "test content",
                           "start_time": timezone.localtime(timezone.now()),
                           "end_time": timezone.localtime(timezone.now()) + timedelta(days=1),
                           "visible": True}


class AssignmentProfessorAPITest(APITestCase):
    def setUp(self):
        professor = self.create_admin()
        self.url = self.reverse("assignment_professor_api")
        self.course_id = Course.objects.create(created_by=professor, **DEFAULT_COURSE_DATA).id
        self.data = copy.deepcopy(DEFAULT_ASSIGNMENT_DATA)
        self.data["course_id"] = self.course_id

    def test_create_assignment(self):
        resp = self.client.post(self.url, data=self.data)
        self.assertSuccess(resp)
        return resp

    def test_delete_assignment(self):
        id = self.test_create_assignment().data["data"]["id"]
        resp = self.client.delete(f"{self.url}?course_id={self.course_id}&assignment_id={id}")
        self.assertSuccess(resp)
        self.assertFalse(Assignment.objects.filter(id=id).exists())

    def test_edit_assignment(self):
        id = self.test_create_assignment().data["data"]["id"]
        update_data = {"id": id,
                       "title": "update title",
                       "content": "update content"}
        data = copy.deepcopy(self.data)
        data.update(update_data)
        resp = self.client.put(self.url, data=data)
        self.assertSuccess(resp)
        resp_data = resp.data["data"]
        self.assertEqual(resp_data["title"], "update title")
        self.assertEqual(resp_data["content"], "update content")

    def test_get_assignment_list(self):
        self.test_create_assignment()
        resp = self.client.get(f"{self.url}?course_id={self.course_id}")
        self.assertSuccess(resp)

    def test_get_one_assignment(self):
        id = self.test_create_assignment().data["data"]["id"]
        resp = self.client.get(f"{self.url}?course_id={self.course_id}&assignment_id={id}")
        self.assertSuccess(resp)


class AssignmentStudentAPITest(APITestCase):
    def setUp(self):
        professor = self.create_admin()
        self.course_id = Course.objects.create(created_by=professor, **DEFAULT_COURSE_DATA).id
        assignment_data = copy.deepcopy(DEFAULT_ASSIGNMENT_DATA)
        assignment_data["course_id"] = self.course_id
        self.assignment_id = Assignment.objects.create(created_by=professor, **assignment_data).id
        student_id = self.create_user("2020123123", "123").id
        Registration.objects.create(user_id=student_id, course_id=self.course_id)
        self.url = self.reverse("assignment_api")

    def test_get_assignment_list(self):
        resp = self.client.get(f"{self.url}?course_id={self.course_id}")
        self.assertSuccess(resp)

    def test_get_one_assignment(self):
        resp = self.client.get(f"{self.url}?course_id={self.course_id}&assignment_id={self.assignment_id}")
        self.assertSuccess(resp)
