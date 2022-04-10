import copy
from datetime import datetime, timedelta

from django.utils import timezone
from group.models import Group

from utils.api.tests import APITestCase

from .models import ContestAnnouncement, ContestRuleType, Contest

from problem.models import ProblemIOMode

DEFAULT_PROBLEM_DATA = {"_id": "A-110", "title": "test", "description": "<p>test</p>", "input_description": "test",
                        "output_description": "test", "time_limit": 1000, "memory_limit": 256, "difficulty": "Level1",
                        "visible": True, "tags": ["test"], "languages": ["C", "C++", "Java", "Python2"], "template": {},
                        "samples": [{"input": "test", "output": "test"}], "spj": False, "spj_language": "C",
                        "spj_code": "", "spj_compile_ok": True, "test_case_id": "499b26290cc7994e0b497212e842ea85",
                        "test_case_score": [{"output_name": "1.out", "input_name": "1.in", "output_size": 0,
                                             "stripped_output_md5": "d41d8cd98f00b204e9800998ecf8427e",
                                             "input_size": 0, "score": 0}],
                        "io_mode": {"io_mode": ProblemIOMode.standard, "input": "input.txt", "output": "output.txt"},
                        "share_submission": False,
                        "rule_type": "ACM", "hint": "<p>test</p>", "source": "test", "bank": False}

DEFAULT_CONTEST_DATA = {"title": "test title", "description": "test description",
                        "requirements": ["SKKU undergrate enrolled 2021 Spring"],
                        "constraints": ["Not Awarded in same past competition"],
                        "scoring": "ACM-ICPC style",
                        "prizes": [{"color": "#FF6663", "name": "Top 2", "reward": "1,000,000 Won"},
                                   {"color": "#FFD700", "name": "3(3~5)", "reward": "500,000 Won"},
                                   {"color": "#C0C0C0", "name": "5(6~10)", "reward": "100,000 Won"},
                                   {"color": "#CD7F32", "name": "10(11~20)", "reward": "50,000 Won"}],
                        "allowed_groups": [],
                        "start_time": timezone.localtime(timezone.now()),
                        "end_time": timezone.localtime(timezone.now()) + timedelta(days=1),
                        "rule_type": ContestRuleType.ACM,
                        "password": "123",
                        "allowed_ip_ranges": [],
                        "bank_filter": [],
                        "visible": True, "real_time_rank": True, "rank_penalty_visible": True}


class ContestAdminAPITest(APITestCase):
    def setUp(self):
        self.super_admin = self.create_super_admin()
        self.url = self.reverse("contest_admin_api")
        self.data = copy.deepcopy(DEFAULT_CONTEST_DATA)

    def test_create_contest(self):
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        return response

    def test_create_contest_with_bank_filter(self):
        self.data["bank_filter"] = [{"level": "Level1", "tag": "", "count": 1}, {"level": "Level2", "tag": "", "count": 3}]
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        return response

    def test_create_contest_with_invalid_cidr(self):
        self.data["allowed_ip_ranges"] = ["127.0.0"]
        resp = self.client.post(self.url, data=self.data)
        self.assertTrue(resp.data["data"].endswith("is not a valid cidr network"))

    def test_create_contest_with_group_not_existing(self):
        self.data["allowed_groups"] = [1]
        response = self.client.post(self.url, data=self.data)
        self.assertFailed(response)

    def test_create_contest_with_group_existing(self):
        group = Group.objects.create(
            created_by=self.super_admin,
            name="SKKUding",
            short_description="post group registration request",
            description="post group registration request",
            is_official=True
        )
        group.members.add(self.super_admin, through_defaults={"is_group_admin": False})
        self.data["allowed_groups"] = [group.id]
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)

    def test_update_contest(self):
        id = self.test_create_contest().data["data"]["id"]
        update_data = {"id": id, "title": "update title",
                       "description": "update description",
                       "password": "12345",
                       "bank_filter": [{"level": "Level1", "tag": "", "count": 1}],
                       "visible": False, "real_time_rank": False}
        data = copy.deepcopy(self.data)
        data.update(update_data)
        response = self.client.put(self.url, data=data)
        self.assertSuccess(response)
        response_data = response.data["data"]
        response_data.pop("prizes")
        data.pop("prizes")
        for k in data.keys():
            if isinstance(data[k], datetime):
                continue
            self.assertEqual(response_data[k], data[k])

    def test_get_contests(self):
        self.test_create_contest()
        response = self.client.get(self.url)
        self.assertSuccess(response)

    def test_get_one_contest(self):
        id = self.test_create_contest().data["data"]["id"]
        response = self.client.get("{}?id={}".format(self.url, id))
        self.assertSuccess(response)


class ContestAPITest(APITestCase):
    def setUp(self):
        user = self.create_admin()
        group = self.create_group(created_by=user)
        data = copy.deepcopy(DEFAULT_CONTEST_DATA)
        data.pop("allowed_groups")
        data.pop("prizes")
        allowed_groups = [group.id]
        allowed_groups_qs = Group.objects.filter(id__in=allowed_groups)
        self.contest = Contest.objects.create(created_by=user, **data)
        self.contest.allowed_groups.set(allowed_groups_qs)
        self.url = self.reverse("contest_api") + "?id=" + str(self.contest.id)

    def test_get_contest_list(self):
        url = self.reverse("contest_list_api")
        response = self.client.get(url + "?limit=10")
        self.assertSuccess(response)
        self.assertEqual(len(response.data["data"]["results"]), 1)

    def test_get_one_contest(self):
        resp = self.client.get(self.url)
        self.assertSuccess(resp)

    def test_regular_user_validate_contest_password(self):
        self.create_user("test", "test123")
        url = self.reverse("contest_password_api")
        resp = self.client.post(url, {"contest_id": self.contest.id, "password": "error_password"})
        self.assertDictEqual(resp.data, {"error": "error", "data": "Wrong password or password expired"})

        resp = self.client.post(url, {"contest_id": self.contest.id, "password": DEFAULT_CONTEST_DATA["password"]})
        self.assertSuccess(resp)

    def test_regular_user_access_contest(self):
        self.create_user("test", "test123")
        url = self.reverse("contest_access_api")
        resp = self.client.get(url + "?contest_id=" + str(self.contest.id))
        self.assertFalse(resp.data["data"]["access"])

        password_url = self.reverse("contest_password_api")
        resp = self.client.post(password_url,
                                {"contest_id": self.contest.id, "password": DEFAULT_CONTEST_DATA["password"]})
        self.assertSuccess(resp)
        resp = self.client.get(self.url)
        self.assertSuccess(resp)

    def test_not_group_member_access_contest(self):
        self.create_user("test2", "test1234")
        url = self.reverse("contest_access_api")
        resp = self.client.get(url + "?contest_id=" + str(self.contest.id))
        self.assertFalse(resp.data["data"]["access"])

        password_url = self.reverse("contest_password_api")
        resp = self.client.post(password_url,
                                {"contest_id": self.contest.id, "password": DEFAULT_CONTEST_DATA["password"]})
        self.assertSuccess(resp)
        resp = self.client.get(self.url)
        self.assertSuccess(resp)


class ContestAnnouncementAdminAPITest(APITestCase):
    def setUp(self):
        self.create_super_admin()
        self.url = self.reverse("contest_announcement_admin_api")
        contest_id = self.create_contest().data["data"]["id"]
        url = self.reverse("contest_problem_admin_api")
        data = copy.deepcopy(DEFAULT_PROBLEM_DATA)
        data["contest_id"] = contest_id
        self.problem = self.client.post(url, data=data).data["data"]
        problem_id = self.problem["id"]
        self.data = {"title": "test title", "content": "test content", "contest_id": contest_id, "visible": True, "problem_id": problem_id}

    def create_contest(self):
        url = self.reverse("contest_admin_api")
        data = DEFAULT_CONTEST_DATA
        return self.client.post(url, data=data)

    def test_create_contest_announcement(self):
        response = self.client.post(self.url, data=self.data)
        self.assertSuccess(response)
        return response

    def test_delete_contest_announcement(self):
        id = self.test_create_contest_announcement().data["data"]["id"]
        response = self.client.delete("{}?id={}".format(self.url, id))
        self.assertSuccess(response)
        self.assertFalse(ContestAnnouncement.objects.filter(id=id).exists())

    def test_get_contest_announcements(self):
        self.test_create_contest_announcement()
        response = self.client.get(self.url + "?contest_id=" + str(self.data["contest_id"]))
        self.assertSuccess(response)

    def test_get_one_contest_announcement(self):
        id = self.test_create_contest_announcement().data["data"]["id"]
        response = self.client.get("{}?id={}".format(self.url, id))
        self.assertSuccess(response)


class ContestAnnouncementListAPITest(APITestCase):
    def setUp(self):
        self.create_super_admin()
        self.url = self.reverse("contest_announcement_api")

    def create_contest_announcements(self):
        contest_id = self.client.post(self.reverse("contest_admin_api"), data=DEFAULT_CONTEST_DATA).data["data"]["id"]
        url = self.reverse("contest_announcement_admin_api")
        self.client.post(url, data={"title": "test title1", "content": "test content1", "contest_id": contest_id, "problem_id": "1"})
        self.client.post(url, data={"title": "test title2", "content": "test content2", "contest_id": contest_id, "problem_id": "1"})
        return contest_id

    def test_get_contest_announcement_list(self):
        contest_id = self.create_contest_announcements()
        response = self.client.get(self.url, data={"contest_id": contest_id})
        self.assertSuccess(response)


class ProblemBankAPITest(APITestCase):
    def create_problems(self):
        problem_data = copy.deepcopy(DEFAULT_PROBLEM_DATA)
        problem_data["bank"] = True
        url = self.reverse("problem_admin_api")
        self.client.post(url, data=problem_data)
        problem_data["_id"] = "A-111"
        self.client.post(url, data=problem_data)
        problem_data["_id"] = "A-112"
        problem_data["difficulty"] = "Level2"
        self.client.post(url, data=problem_data)

    def test_create_problem_bank(self):
        self.create_super_admin()
        # create problembank contest
        contest_data = copy.deepcopy(DEFAULT_CONTEST_DATA)
        contest_data["password"] = ""
        contest_data["bank_filter"] = [{"level": "Level1", "tag": "", "count": 1}, {"level": "Level2", "tag": "", "count": 1}]
        contest = self.client.post(self.reverse("contest_admin_api"), data=contest_data).data["data"]

        self.create_problems()

        self.create_user("2018123123", "123123")
        url = self.reverse("contest_bank_api")
        response = self.client.post(url, data={"contest_id": contest["id"]})
        self.assertSuccess(response)
