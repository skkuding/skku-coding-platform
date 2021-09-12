import time

from unittest import mock
from datetime import timedelta
from copy import deepcopy

from django.contrib import auth
from django.utils.timezone import now

from utils.api.tests import APIClient, APITestCase
from utils.shortcuts import rand_str
from utils.cache import cache
from utils.constants import CacheKey
from options.options import SysOptions

from .models import AdminType, ProblemPermission, User


class PermissionDecoratorTest(APITestCase):
    def setUp(self):
        self.regular_user = User.objects.create(username="regular_user")
        self.admin = User.objects.create(username="admin")
        self.super_admin = User.objects.create(username="super_admin")
        self.request = mock.MagicMock()
        self.request.user.is_authenticated = mock.MagicMock()

    def test_login_required(self):
        self.request.user.is_authenticated.return_value = False

    def test_admin_required(self):
        pass

    def test_super_admin_required(self):
        pass


class DuplicateUserCheckAPITest(APITestCase):
    def setUp(self):
        user = self.create_user("2020123456", "test123", login=False)
        user.email = "test@skku.edu"
        user.save()
        self.url = self.reverse("check_username_or_email")

    def test_duplicate_username(self):
        resp = self.client.post(self.url, data={"username": "2020123456"})
        self.assertEqual(resp.data["data"]["username"], 1)

    def test_ok_username(self):
        resp = self.client.post(self.url, data={"username": "2020987654"})
        data = resp.data["data"]
        self.assertFalse(data["username"])

    def test_duplicate_email(self):
        resp = self.client.post(self.url, data={"email": "test@skku.edu"})
        self.assertEqual(resp.data["data"]["email"], 1)
        resp = self.client.post(self.url, data={"email": "Test@Skku.edu"})
        self.assertEqual(resp.data["data"]["email"], 1)

    def test_ok_email(self):
        resp = self.client.post(self.url, data={"email": "aa@skku.edu"})
        self.assertFalse(resp.data["data"]["email"])


class WrongFormatUserCheckAPITest(APITestCase):
    def setUp(self):
        self.url = self.reverse("check_username_or_email")

    def test_wrong_format_username(self):
        resp = self.client.post(self.url, data={"username": "202012345"})
        data = resp.data["data"]
        self.assertEqual(data["username"], 2)
        resp = self.client.post(self.url, data={"username": "20201234567"})
        data = resp.data["data"]
        self.assertEqual(data["username"], 2)
        resp = self.client.post(self.url, data={"username": "2020hahaha"})
        data = resp.data["data"]
        self.assertEqual(data["username"], 2)
        resp = self.client.post(self.url, data={"username": "1234567890"})
        data = resp.data["data"]
        self.assertEqual(data["username"], 2)

    def test_not_university_email(self):
        resp = self.client.post(self.url, data={"email": "hello@gmail.com"})
        self.assertEqual(resp.data["data"]["email"], 2)


class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.username = self.password = "2020222000"
        self.user = self.create_user(username=self.username, password=self.password, login=False)
        self.login_url = self.reverse("user_login_api")

    def test_login_with_correct_info(self):
        response = self.client.post(self.login_url,
                                    data={"username": self.username, "password": self.password})
        self.assertDictEqual(response.data, {"error": None, "data": "Succeeded"})

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_login_with_correct_info_upper_username(self):
        resp = self.client.post(self.login_url, data={"username": self.username.upper(), "password": self.password})
        self.assertDictEqual(resp.data, {"error": None, "data": "Succeeded"})
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_login_with_wrong_info(self):
        response = self.client.post(self.login_url,
                                    data={"username": self.username, "password": "invalid_password"})
        self.assertDictEqual(response.data, {"error": "error", "data": "Invalid username or password"})

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_disabled(self):
        self.user.is_disabled = True
        self.user.save()
        resp = self.client.post(self.login_url, data={"username": self.username,
                                                      "password": self.password})
        self.assertDictEqual(resp.data, {"error": "error", "data": "Your account has been disabled"})


class CaptchaTest(APITestCase):
    def _set_captcha(self, session):
        captcha = rand_str(4)
        session["_django_captcha_key"] = captcha
        session["_django_captcha_expires_time"] = int(time.time()) + 30
        session.save()
        return captcha


class TokenTest(APITestCase):
    def _set_token_and_email(self, email):
        self.email_auth_token = rand_str()
        self.token_cache_key = f"{CacheKey.auth_token_cache}:{self.email_auth_token}"
        self.email_cache_key = f"{CacheKey.auth_email_cache}:{self.email_auth_token}"
        cache.set(self.token_cache_key, self.email_auth_token, 1200)
        cache.set(self.email_cache_key, email, 1200)
        return self.email_auth_token

    def _delete_token_and_email(self):
        cache.delete(self.token_cache_key)
        cache.delete(self.email_cache_key)


class UserRegisterAPITest(TokenTest):
    def setUp(self):
        self.client = APIClient()
        self.register_url = self.reverse("user_register_api")

        self.data = {"username": "2020111111", "password": "testuserpassword",
                     "real_name": "real_name", "email": "test@skku.edu",
                     "major": "Computer Science (컴퓨터공학과)",
                     "token": self._set_token_and_email("test@skku.edu")}

    def test_website_config_limit(self):
        SysOptions.allow_register = False
        resp = self.client.post(self.register_url, data=self.data)
        self.assertDictEqual(resp.data, {"error": "error", "data": "Register function has been disabled by admin"})

    def test_register_with_correct_info(self):
        response = self.client.post(self.register_url, data=self.data)
        self.assertDictEqual(response.data, {"error": None, "data": "Succeeded"})

    def test_username_already_exists(self):
        self.test_register_with_correct_info()

        self.data["email"] = "test1@skku.edu"
        self.data["token"] = self._set_token_and_email(self.data["email"])
        response = self.client.post(self.register_url, data=self.data)
        self._delete_token_and_email()
        self.assertDictEqual(response.data, {"error": "error", "data": "Username already exists"})

    def test_register_with_invalid_token(self):
        self.data["token"] = "abcde"
        resp = self.client.post(self.register_url, data=self.data)
        self._delete_token_and_email()
        self.assertDictEqual(resp.data, {"error": "error", "data": "Token does not exist"})

    def test_register_with_invalid_email(self):
        self.data["email"] = "invalid@skku.edu"
        resp = self.client.post(self.register_url, data=self.data)
        self._delete_token_and_email()
        self.assertDictEqual(resp.data, {"error": "error", "data": "It is not authenticated email"})


class UserProfileAPITest(APITestCase):
    def setUp(self):
        self.url = self.reverse("user_profile_api")

    def test_get_profile_without_login(self):
        resp = self.client.get(self.url)
        self.assertDictEqual(resp.data, {"error": None, "data": None})

    def test_get_profile(self):
        self.create_user("2020222000", "test123")
        resp = self.client.get(self.url)
        self.assertSuccess(resp)

    def test_update_profile(self):
        self.create_user("2020222000", "test123")
        update_data = {"real_name": "zemal", "submission_number": 233, "language": "en-US"}
        resp = self.client.put(self.url, data=update_data)
        self.assertSuccess(resp)
        data = resp.data["data"]
        self.assertEqual(data["real_name"], "zemal")
        self.assertEqual(data["submission_number"], 0)
        self.assertEqual(data["language"], "en-US")


@mock.patch("account.views.oj.send_email_async.send")
class ApplyResetPasswordAPITest(CaptchaTest):
    def setUp(self):
        self.create_user("2020222000", "test123", login=False)
        user = User.objects.first()
        user.email = "test@g.skku.edu"
        user.save()
        self.url = self.reverse("apply_reset_password_api")
        self.data = {"email": "test@g.skku.edu", "captcha": self._set_captcha(self.client.session)}

    def _refresh_captcha(self):
        self.data["captcha"] = self._set_captcha(self.client.session)

    def test_apply_reset_password(self, send_email_send):
        resp = self.client.post(self.url, data=self.data)
        self.assertSuccess(resp)
        send_email_send.assert_called()

    def test_apply_reset_password_twice_in_20_mins(self, send_email_send):
        self.test_apply_reset_password()
        send_email_send.reset_mock()
        self._refresh_captcha()
        resp = self.client.post(self.url, data=self.data)
        self.assertDictEqual(resp.data, {"error": "error", "data": "You can only reset password once per 20 minutes"})
        send_email_send.assert_not_called()

    def test_apply_reset_password_again_after_20_mins(self, send_email_send):
        self.test_apply_reset_password()
        user = User.objects.first()
        user.reset_password_token_expire_time = now() - timedelta(minutes=21)
        user.save()
        self._refresh_captcha()
        self.test_apply_reset_password()


class ResetPasswordAPITest(CaptchaTest):
    def setUp(self):
        self.create_user("2020222000", "test123", login=False)
        self.url = self.reverse("reset_password_api")
        user = User.objects.first()
        user.reset_password_token = "online_judge?"
        user.reset_password_token_expire_time = now() + timedelta(minutes=20)
        user.save()
        self.data = {"token": user.reset_password_token,
                     "captcha": self._set_captcha(self.client.session),
                     "password": "test456"}

    def test_reset_password_with_correct_token(self):
        resp = self.client.post(self.url, data=self.data)
        self.assertSuccess(resp)
        self.assertTrue(self.client.login(username="2020222000", password="test456"))

    def test_reset_password_with_invalid_token(self):
        self.data["token"] = "aaaaaaaaaaa"
        resp = self.client.post(self.url, data=self.data)
        self.assertDictEqual(resp.data, {"error": "error", "data": "Token does not exist"})

    def test_reset_password_with_expired_token(self):
        user = User.objects.first()
        user.reset_password_token_expire_time = now() - timedelta(seconds=30)
        user.save()
        resp = self.client.post(self.url, data=self.data)
        self.assertDictEqual(resp.data, {"error": "error", "data": "Token has expired"})


class UserChangeEmailAPITest(APITestCase):
    def setUp(self):
        self.url = self.reverse("user_change_email_api")
        self.user = self.create_user("2020222000", "test123")
        self.new_mail = "test@skku.edu"
        self.data = {"password": "test123", "new_email": self.new_mail}

    def test_change_email_success(self):
        resp = self.client.post(self.url, data=self.data)
        self.assertSuccess(resp)

    def test_wrong_password(self):
        self.data["password"] = "aaaa"
        resp = self.client.post(self.url, data=self.data)
        self.assertDictEqual(resp.data, {"error": "error", "data": "Wrong password"})

    def test_duplicate_email(self):
        u = self.create_user("aa", "bb", login=False)
        u.email = self.new_mail
        u.save()
        resp = self.client.post(self.url, data=self.data)
        self.assertDictEqual(resp.data, {"error": "error", "data": "The email is owned by other account"})


class UserChangePasswordAPITest(APITestCase):
    def setUp(self):
        self.url = self.reverse("user_change_password_api")

        # Create user at first
        self.username = "2020222000"
        self.old_password = "testuserpassword"
        self.new_password = "new_password"
        self.user = self.create_user(username=self.username, password=self.old_password, login=False)

        self.data = {"old_password": self.old_password, "new_password": self.new_password}

    def test_login_required(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data, {"error": "permission-denied", "data": "Please login first"})

    def test_valid_ola_password(self):
        self.assertTrue(self.client.login(username=self.username, password=self.old_password))
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data, {"error": None, "data": "Succeeded"})
        self.assertTrue(self.client.login(username=self.username, password=self.new_password))

    def test_invalid_old_password(self):
        self.assertTrue(self.client.login(username=self.username, password=self.old_password))
        self.data["old_password"] = "invalid"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.data, {"error": "error", "data": "Invalid old password"})


class ProfileProblemDisplayIDRefreshAPITest(APITestCase):
    def setUp(self):
        pass


class AdminUserTest(APITestCase):
    def setUp(self):
        self.user = self.create_super_admin(login=True)
        self.username = self.password = "2015135790"
        self.regular_user = self.create_user(username=self.username, password=self.password, login=False)
        self.url = self.reverse("user_admin_api")
        self.data = {"id": self.regular_user.id, "username": self.username, "real_name": "test_name",
                     "email": "example@skku.edu", "major": "Computer Science (컴퓨터공학과)",
                     "admin_type": AdminType.REGULAR_USER, "problem_permission": ProblemPermission.OWN,
                     "is_disabled": False}

    def test_user_list(self):
        response = self.client.get(self.url)
        self.assertSuccess(response)

    def test_edit_user_successfully(self):
        response = self.client.put(self.url, data=self.data)
        self.assertSuccess(response)
        resp_data = response.data["data"]
        self.assertEqual(resp_data["username"], self.username)
        self.assertEqual(resp_data["email"], "example@skku.edu")
        self.assertEqual(resp_data["major"], "Computer Science (컴퓨터공학과)")
        self.assertEqual(resp_data["is_disabled"], False)
        self.assertEqual(resp_data["problem_permission"], ProblemPermission.NONE)

        self.assertTrue(self.regular_user.check_password("2015135790"))

    def test_edit_user_password(self):
        data = self.data
        new_password = "testpassword"
        data["password"] = new_password
        response = self.client.put(self.url, data=data)
        self.assertSuccess(response)
        user = User.objects.get(id=self.regular_user.id)
        self.assertFalse(user.check_password(self.password))
        self.assertTrue(user.check_password(new_password))

    def test_import_users(self):
        data = {"users": [["user1", "pass1", "eami1@skku.edu"],
                          ["user2", "pass3", "eamil3@skku.edu"]]
                }
        resp = self.client.post(self.url, data)
        self.assertSuccess(resp)
        # successfully created 2 users
        self.assertEqual(User.objects.all().count(), 4)

    def test_import_duplicate_user(self):
        data = {"users": [["user1", "pass1", "eami1@skku.edu"],
                          ["user1", "pass1", "eami1@skku.edu"]]
                }
        resp = self.client.post(self.url, data)
        self.assertFailed(resp, "DETAIL:  Key (username)=(user1) already exists.")
        # no user is created
        self.assertEqual(User.objects.all().count(), 2)

    def test_delete_users(self):
        self.test_import_users()
        user_ids = User.objects.filter(username__in=["user1", "user2"]).values_list("id", flat=True)
        user_ids = ",".join([str(id) for id in user_ids])
        resp = self.client.delete(self.url + "?id=" + user_ids)
        self.assertSuccess(resp)
        self.assertEqual(User.objects.all().count(), 2)


class GenerateUserAPITest(APITestCase):
    def setUp(self):
        self.create_super_admin()
        self.url = self.reverse("generate_user_api")
        self.data = {
            "number_from": 100, "number_to": 105,
            "prefix": "pre", "suffix": "suf",
            "default_email": "test@test.com",
            "password_length": 8
        }

    def test_error_case(self):
        data = deepcopy(self.data)
        data["prefix"] = "t" * 16
        data["suffix"] = "s" * 14
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.data["data"], "Username should not more than 32 characters")

        data2 = deepcopy(self.data)
        data2["number_from"] = 106
        resp = self.client.post(self.url, data=data2)
        self.assertEqual(resp.data["data"], "Start number must be lower than end number")

    @mock.patch("account.views.admin.xlsxwriter.Workbook")
    def test_generate_user_success(self, mock_workbook):
        resp = self.client.post(self.url, data=self.data)
        self.assertSuccess(resp)
        mock_workbook.assert_called()
