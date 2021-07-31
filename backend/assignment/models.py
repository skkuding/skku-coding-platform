from django.db import models
from django.utils.timezone import now

from course.models import Course
from account.models import User
from utils.models import RichTextField
# Create your models here.
class Assignment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField()
    content = RichTextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    @property
    def status(self):
        if self.start_time > now():
            # NOT_START return 1
            return "1"
        elif self.end_time < now():
            # ENDED return -1
            return "-1"
        else:
            # UNDERWAY return 0
            return "0"

    class Meta:
        db_table = "assignment"
        ordering = ("-start_time",)