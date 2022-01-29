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


class UserGroup(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    description = RichTextField()
    is_official = models.BooleanField()
    # logo = ImageField()

    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    admin_members = models.ManyToManyField(User, related_name="admin_groups")
    members = models.ManyToManyField(User, related_name="groups")

    class Meta:
        db_table = "user_group"


class GroupApplication(models.Model):
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField()

    class Meta:
        db_table = "group_application"
