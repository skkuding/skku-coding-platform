from django.db import models

from course.models import Course
from account.models import User
from utils.models import RichTextField
# Create your models here.
class Assignment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField()
    description = RichTextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = "assignment"
        ordering = ("-start_time",)