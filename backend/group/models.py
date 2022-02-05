# from django.forms import ImageField
from django.db import models

from account.models import User
from utils.models import RichTextField


class GroupRegistrationRequest(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    description = RichTextField()
    is_official = models.BooleanField()

    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "group_registration_request"


class Group(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    description = RichTextField()
    is_official = models.BooleanField()
    # logo = ImageField()

    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    members = models.ManyToManyField(User, related_name="groups", through="GroupMember", through_fields=("group", "user"))

    class Meta:
        db_table = "group"


class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    is_group_admin = models.BooleanField(default=False)


class GroupMemberJoin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField()

    class Meta:
        db_table = "group_member_join"
