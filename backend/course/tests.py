import copy
from utils.api.tests import APITestCase

from .models import Course, Registration

DEFAULT_COURSE_DATA = {"title": "Test",
                       "course_code": "TESTCODE12",
                       "class_number": 43,
                       "registered_year": 2021,
                       "semester": 1}


class CourseProfessorAPITest(APITestCase):
    def setUp(self):
        self.create_admin()
        self.url = self.reverse("course_professor_api")
        self.data = copy.deepcopy(DEFAULT_COURSE_DATA)

    def test_get_course_list(self):
        self.test_create_course()
        res = self.client.get(self.url)
        self.assertSuccess(res)

    def test_get_course(self):
        id = self.test_create_course().data["data"]["id"]
        res = self.client.get(f"{self.url}?id={id}")
        self.assertSuccess(res)

    def test_create_course(self):
        res = self.client.post(self.url, data=self.data)
        self.assertSuccess(res)
        return res

    def test_edit_course(self):
        id = self.test_create_course().data["data"]["id"]
        update_data = {"id": id,
                       "title": "update title",
                       "course_code": "UPDATE12",
                       "class_number": 12,
                       "registered_year": 2022,
                       "semester": 0}
        res = self.client.put(self.url, data=update_data)
        self.assertSuccess(res)
        res_data = res.data["data"]
        for k in update_data.keys():
            self.assertEqual(res_data[k], update_data[k])

    def test_delete_course(self):
        id = self.test_create_course().data["data"]["id"]
        res = self.client.delete(f"{self.url}?id={id}")
        self.assertSuccess(res)
        self.assertFalse(Course.objects.filter(id=id).exists())


class CourseStudentAPITest(APITestCase):
    def setUp(self):
        professor = self.create_admin()
        self.course = Course.objects.create(created_by=professor, title="title", course_code="code", class_number=12, registered_year=2021, semester=0)
        self.url = self.reverse("course_api")
        self.user = self.create_user("user", "password")
        Registration.objects.create(user_id=self.user.id, course_id=self.course.id)

    def test_get_course_list(self):
        res = self.client.get(self.url)
        self.assertSuccess(res)

    def test_get_course(self):
        res = self.client.get(f"{self.url}?id={self.course.id}")
        self.assertSuccess(res)


class StudentManagementAPITest(APITestCase):
    def setUp(self):
        self.student = self.create_user("2016313683", "password")
        self.create_user("2011111111", "password")
        self.create_user("2011111112", "password")
        self.professor = self.create_admin()
        self.course = Course.objects.create(created_by=self.professor, title="title", course_code="code", class_number=12, registered_year=2021, semester=0)
        self.registration = Registration.objects.create(user_id=self.student.id, course_id=self.course.id)
        self.url = self.reverse("student_management_api")

    def test_get_registraion_list(self):
        res = self.client.get(f"{self.url}?course_id={self.course.id}")
        self.assertSuccess(res)

    def test_get_regitstration_count(self):
        res = self.client.get(f"{self.url}?course_id={self.course.id}&count=1")
        self.assertTrue("total_students" in res.data["data"])
        res = self.client.get(f"{self.url}?course_id={self.course.id}&count=0")
        self.assertFalse("total_students" in res.data["data"])

    def test_create_registration(self):
        res = self.client.post(self.url, data={"username": ["2011111111"], "course_id": self.course.id})
        self.assertSuccess(res)

    def test_create_multiple_registration(self):
        res = self.client.post(self.url, data={"username": ["2011111111", "2011111112"], "course_id": self.course.id})
        self.assertSuccess(res)

    def test_create_registration_user_not_exist(self):
        res = self.client.post(self.url, data={"username": ["123123"], "course_id": self.course.id})
        self.assertTrue(res.data["data"]["error"] is not None)
        self.assertSuccess(res)

    def test_create_registration_already_registered_user(self):
        res = self.client.post(self.url, data={"username": ["2016313683"], "course_id": self.course.id})
        self.assertTrue(res.data["data"]["error"] is not None)
        self.assertSuccess(res)

    def test_edit_registration(self):
        id = self.registration.id
        course = Course.objects.create(created_by=self.professor, title="title2", course_code="code2", class_number=12, registered_year=2021, semester=1)
        res = self.client.put(self.url, data={"registration_id": id, "course_id": course.id})
        self.assertSuccess(res)

    def test_delete_registration(self):
        id = self.registration.id
        res = self.client.delete(f"{self.url}?registration_id={id}")
        self.assertSuccess(res)
        self.assertFalse(Registration.objects.filter(id=id).exists())
