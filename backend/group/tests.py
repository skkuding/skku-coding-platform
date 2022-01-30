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
        self.assertSuccess(res)

    def test_group_registration_response_reject(self):
        res = self.client.post(self.url, data={
            "accept": False,
            "request_id": self.group_registration_request.id
        })
        self.assertSuccess(res)


class GroupAPITest(APITestCase):
    def setUp(self):
        admin = self.create_admin()
        user = self.create_user("user", "useruser")
        super_admin = self.create_super_admin()

        self.url = self.reverse("group_api") + "?username=" + str(super_admin.username)
        group_admin = UserGroup.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group_admin.admin_members.add(super_admin)

        group = UserGroup.objects.create(
            created_by=admin,
            name="AdminClub",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.admin_members.add(admin)
        group.members.add(super_admin)

        other_group = UserGroup.objects.create(
            created_by=user,
            name="UserClub",
            short_description="post group registration request",
            description="post group registration request",
            is_official=False
        )
        other_group.members.add(user)

    def test_get_group_list(self):
        res = self.client.get(self.url)
        self.assertSuccess(res)


class GroupDetailAPITest(APITestCase):
    def setUp(self):
        super_admin = self.create_super_admin()
        group = UserGroup.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.admin_members.add(super_admin)
        self.url = self.reverse("group_detail_api") + "?id=" + str(group.id)

    def test_get_group_detail(self):
        res = self.client.get(self.url)
        self.assertSuccess(res)


class GroupApplicationAPITest(APITestCase):
    def setUp(self):
        super_admin = self.create_super_admin()
        group = UserGroup.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.admin_members.add(super_admin)

        self.group_id = group.id
        self.url = self.reverse("group_application_api")

    def test_post_group_application(self):
        res = self.client.post(self.url, data={
            "group_id": self.group_id,
            "description": "I have to be in there!"
        })
        self.assertSuccess(res)

    def test_delete_group_application_accept(self):
        application = self.client.post(self.url, data={
            "group_id": self.group_id,
            "description": "I have to be in there!"
        })
        res = self.client.delete("{}?group_id={}&application_id={}&accept={}".format(self.url, self.group_id, application.data["data"]["id"], True))
        self.assertSuccess(res)

    def test_delete_group_application_reject(self):
        application = self.client.post(self.url, data={
            "group_id": self.group_id,
            "description": "I have to be in there!"
        })
        res = self.client.delete("{}?group_id={}&application_id={}&accept={}".format(self.url, self.group_id, application.data["data"]["id"], False))
        self.assertSuccess(res)
