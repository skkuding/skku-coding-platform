from django.db import models
from django.db.models import JSONField


class SysOptions(models.Model):
    key = models.TextField(unique=True, db_index=True)
    value = JSONField()
