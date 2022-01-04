from django.db import models

from account.models import User


class Course(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    course_code = models.TextField()
    class_number = models.IntegerField()
    registered_year = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        db_table = "course"
        ordering = ("-registered_year",)


class Registration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "registration"

class Question(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    create_time = models.DateTimeField()
    last_update_time = models.DateTimeField()
    status = models.BooleanField()

    class Meta:
        db_table = "question"
        ordering = ("-create_time",)