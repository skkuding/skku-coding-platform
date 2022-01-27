from django.forms import ImageField
from django.db import models

from account.models import User
from utils.models import RichTextField


class UserGroup(models.Model):
    title = models.TextField()
    description = RichTextField()
    logo = ImageField()

    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    admin_members = models.ManyToManyField(User, related_name="group_admin_members")
    members = models.ManyToManyField(User, related_name="group_members")

    class Meta:
        db_table = "user_group"


class GroupApplication(models.Model):
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField()
