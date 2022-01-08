from django.db import models

from account.models import User


class AdminType(object):
    PROFESSOR = "Professor"
    CREATOR = "Creator"
    NONE = "None"


# created_by, course_id, title, content, create_time, last_update_time, status
class Question(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    
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

    class Meta:
        db_table = "answer"
        ordering = ("-create_time",)