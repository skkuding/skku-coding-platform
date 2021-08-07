from django.db import models
from datetime import date

from account.models import User

# Create your models here.
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