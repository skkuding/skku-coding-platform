from django.db import models
from django.utils.timezone import now

from course.models import Course
from account.models import User
from utils.models import RichTextField
from utils.constants import AssignmentStatus


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
            return AssignmentStatus.ASSIGNMENT_NOT_START
        elif self.end_time < now():
            # ENDED return -1
            return AssignmentStatus.ASSIGNMENT_ENDED
        else:
            # UNDERWAY return 0
            return AssignmentStatus.ASSIGNMENT_UNDERWAY

    def problem_details_permission(self, user):
        return user.is_authenticated and user.is_assignment_admin(self)

    class Meta:
        db_table = "assignment"
        ordering = ("-start_time",)
