from utils.api.tests import APITestCase
from .models import GroupRegistrationRequest, UserGroup


class GroupRegistrationRequestAPITest(APITestCase):
    def setUp(self):
        self.create_super_admin()
        self.url = self.reverse("group_registration_request_api")
        self.data = {
            "name": "SKKUding",
            "short_description": "post group registration request",
            "description": "post group registration request",
            "is_official": "true"
        }

    def test_create_group_registration_request(self):
        res = self.client.post(self.url, data=self.data)
        self.assertSuccess(res)


class AdminGroupRegistrationRequestAPITest(APITestCase):
    def setUp(self):
        super_admin = self.create_super_admin()
        self.url = self.reverse("group_registration_request_admin_api")
        self.group_registration_request = GroupRegistrationRequest.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )

    def test_get_admin_group_registration_request(self):
        res = self.client.get(self.url)
        self.assertSuccess(res)


class AdminGroupRegistrationResponseAPITest(APITestCase):
    def setUp(self):
        super_admin = self.create_super_admin()
        self.url = self.reverse("group_registration_response_admin_api")
        self.group_registration_request = GroupRegistrationRequest.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )

    def test_group_registration_response_accept(self):
        res = self.client.post(self.url, data={
            "accept": True,
            "request_id": self.group_registration_request.id
        })
        print(self.client.get(self.reverse("group_api") + "?username=" + "root").data)
        self.assertSuccess(res)

    def test_group_registration_response_reject(self):
        res = self.client.post(self.url, data={
            "accept": False,
            "request_id": self.group_registration_request.id
        })
        self.assertSuccess(res)


class GroupAPITest(APITestCase):
    def setUp(self):
        super_admin = self.create_super_admin()
        self.url = self.reverse("group_api") + "?username=" + str(super_admin.username)
        self.group_registration_request = UserGroup.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        self.group_registration_request.admin_members.add(super_admin)

    def test_get_group_list(self):
        res = self.client.get(self.url)
        self.assertSuccess(res)
