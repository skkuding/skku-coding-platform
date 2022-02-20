from django.db import models

from account.models import User
from course.models import Course


class AdminType(object):
    PROFESSOR = "Professor"
    CREATOR = "Creator"
    NONE = "None"


class Question(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        db_table = "question"
        ordering = ("-create_time",)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    admin_type = models.TextField(default=AdminType.NONE)

    class Meta:
        db_table = "answer"
        ordering = ("-create_time",)

    def update_admin_type(self, user):
        if user.is_authenticated and user.is_admin_role():
            self.admin_type = AdminType.PROFESSOR
        elif user.is_question_admin(self.question):
            self.admin_type = AdminType.CREATOR
        self.save(update_fields=["admin_type"])

    def name(self):
        if self.admin_type == AdminType.PROFESSOR:
            return self.created_by.userprofile.real_name
        return self.created_by.username
