from utils.api.tests import APITestCase
from .models import GroupRegistrationRequest, Group


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

    def test_create_registration_request_duplicate_group_name(self):
        self.client.post(self.url, data=self.data)
        res = self.client.post(self.url, data=self.data)
        self.assertFailed(res, msg="Duplicate group name")


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

    def test_delete_group_registration_request_accept(self):
        res = self.client.delete(self.url + "?accept=True&request_id=" + str(self.group_registration_request.id))
        self.assertSuccess(res)

    def test_delete_group_registration_request_reject(self):
        res = self.client.delete(self.url + "?accept=False&request_id=" + str(self.group_registration_request.id))
        self.assertSuccess(res)

    def test_delete_group_registration_double_reject_fail(self):
        self.client.delete(self.url + "?accept=False&request_id=" + str(self.group_registration_request.id))
        res = self.client.delete(self.url + "?accept=False&request_id=" + str(self.group_registration_request.id))
        self.assertFailed(res, msg="Invalid group registration request id")

    def test_delete_group_registration_double_accept_fail(self):
        self.client.delete(self.url + "?accept=True&request_id=" + str(self.group_registration_request.id))
        res = self.client.delete(self.url + "?accept=True&request_id=" + str(self.group_registration_request.id))
        self.assertFailed(res, msg="Invalid group registration request id")


class GroupAPITest(APITestCase):
    def setUp(self):
        admin = self.create_admin()
        user = self.create_user("user", "useruser")
        super_admin = self.create_super_admin()

        self.url = self.reverse("group_api")
        group_admin = Group.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group_admin.members.add(super_admin, through_defaults={"is_group_admin": True})

        group = Group.objects.create(
            created_by=admin,
            name="AdminClub",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.members.add(admin, through_defaults={"is_group_admin": False})
        group.members.add(super_admin)

        other_group = Group.objects.create(
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
        group = Group.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.members.add(super_admin, through_defaults={"is_group_admin": True})
        self.url = self.reverse("group_api") + "?id=" + str(group.id)

    def test_get_group_detail(self):
        res = self.client.get(self.url)
        self.assertSuccess(res)


class GroupMemberAPITest(APITestCase):
    def setUp(self):
        admin = self.create_admin()
        super_admin = self.create_super_admin()

        group = Group.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.members.add(super_admin, through_defaults={"is_group_admin": True})
        group.members.add(admin)
        self.url = self.reverse("group_member_api")

        self.group_id = group.id
        self.admin_id = admin.id
        self.super_admin_id = super_admin.id

    def test_change_group_permission_into_admin(self):
        res = self.client.put(self.url, data={
            "group_id": self.group_id,
            "user_id": self.admin_id,
            "is_group_admin": True
        })
        self.assertSuccess(res)

    def test_change_group_permission_into_common(self):
        res = self.client.put(self.url, data={
            "group_id": self.group_id,
            "user_id": self.admin_id,
            "is_group_admin": False
        })
        self.assertSuccess(res)

    def test_change_group_permission_of_creator_into_common_fail(self):
        self.client.login(username="admin", password="admin")
        res = self.client.put(self.url, data={
            "group_id": self.group_id,
            "user_id": self.super_admin_id,
            "is_group_admin": False
        })
        self.assertFailed(res)

    def test_delete_group_member_success(self):
        res = self.client.delete(self.url + "?group_id={}&user_id={}".format(self.group_id, self.admin_id))
        self.assertSuccess(res)

    def test_delete_group_member_no_permission_fail(self):
        res = self.client.delete(self.url + "?group_id={}&user_id={}".format(self.group_id, self.super_admin_id))
        self.assertFailed(res)

    def test_delete_group_member_cannot_delete_admin_fail(self):
        self.client.put(self.url, data={
            "group_id": self.group_id,
            "user_id": self.admin_id,
            "is_group_admin": True
        })
        res = self.client.delete(self.url + "?group_id={}&user_id={}".format(self.group_id, self.admin_id))
        self.assertFailed(res)


class GroupMemberJoinAPITest(APITestCase):
    def setUp(self):
        super_admin = self.create_super_admin()
        self.create_admin()

        group = Group.objects.create(
            created_by=super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.members.add(super_admin, through_defaults={"is_group_admin": True})

        self.group_id = group.id
        self.url = self.reverse("group_member_join_api")

    def test_post_group_member_join(self):
        self.client.login(username="admin", password="admin")
        res = self.client.post(self.url, data={
            "group_id": self.group_id,
            "description": "I have to be in there!"
        })
        self.assertSuccess(res)

    def test_delete_group_member_join_accept(self):
        self.client.login(username="admin", password="admin")
        member_join = self.client.post(self.url, data={
            "group_id": self.group_id,
            "description": "I have to be in there!"
        })
        self.client.login(username="root", password="root")
        res = self.client.delete("{}?group_id={}&member_join_id={}&accept={}".format(self.url, self.group_id, member_join.data["data"]["id"], True))
        self.assertSuccess(res)

    def test_delete_group_member_join_reject(self):
        self.client.login(username="admin", password="admin")
        member_join = self.client.post(self.url, data={
            "group_id": self.group_id,
            "description": "I have to be in there!"
        })
        self.client.login(username="root", password="root")
        res = self.client.delete("{}?group_id={}&member_join_id={}&accept={}".format(self.url, self.group_id, member_join.data["data"]["id"], False))
        self.assertSuccess(res)
