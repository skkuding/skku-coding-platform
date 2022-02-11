from django.urls import reverse
from django.test.testcases import TestCase
from rest_framework.test import APIClient

from account.models import AdminType, ProblemPermission, User, UserProfile
from group.models import Group


class APITestCase(TestCase):
    client_class = APIClient

    def create_user(self, username, password, admin_type=AdminType.REGULAR_USER, login=True,
                    problem_permission=ProblemPermission.NONE):
        user = User.objects.create(username=username, admin_type=admin_type, problem_permission=problem_permission)
        user.set_password(password)
        UserProfile.objects.create(user=user)
        user.save()
        if login:
            self.client.login(username=username, password=password)
        return user

    def create_admin(self, username="admin", password="admin", login=True):
        return self.create_user(username=username, password=password, admin_type=AdminType.ADMIN,
                                problem_permission=ProblemPermission.OWN,
                                login=login)

    def create_super_admin(self, username="root", password="root", login=True):
        return self.create_user(username=username, password=password, admin_type=AdminType.SUPER_ADMIN,
                                problem_permission=ProblemPermission.ALL, login=login)

    def create_group(self, created_by, name="SKKUding", short_description="post group registration request", description="post group registration request", is_official=True):
        group = Group.objects.create(created_by=created_by, name=name, short_description=short_description, description=description, is_official=is_official)
        group.members.add(created_by, through_defaults={"is_group_admin": True})
        return group

    def add_group_member(self, group, member, is_admin=False):
        group.members.add(member, through_defaults={"is_group_admin": is_admin})
        return group

    def reverse(self, url_name, *args, **kwargs):
        return reverse(url_name, *args, **kwargs)

    def assertSuccess(self, response):
        if not response.data["error"] is None:
            raise AssertionError("response with errors, response: " + str(response.data))

    def assertFailed(self, response, msg=None):
        self.assertTrue(response.data["error"] is not None)
        if msg:
            self.assertEqual(response.data["data"], msg)
