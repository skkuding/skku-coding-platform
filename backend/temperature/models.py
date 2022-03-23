from django.db import models
from problem.models import Problem
from account.models import User


class JudgeStatus:
    COMPILE_ERROR = -2
    WRONG_ANSWER = -1
    ACCEPTED = 0
    CPU_TIME_LIMIT_EXCEEDED = 1
    REAL_TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    PENDING = 6
    JUDGING = 7
    PARTIALLY_ACCEPTED = 8


class ProblemScore:
    scores = {
        "LEVEL1": 8,
        "LEVEL2": 16,
        "LEVEL3": 32,
        "LEVEL4": 64,
        "LEVEL5": 128,
        "LEVEL6": 256,
        "LEVEL7": 512,
    }


class Temperature(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    temperature = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "temperature"
        unique_together = (("user", "date"),)
        ordering = ("-date",)


class SolvedProblem(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, null=True, on_delete=models.CASCADE)
    score = models.IntegerField()
    solved_time = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "solvedproblem"
        unique_together = (("user", "problem"),)
        ordering = ("-solved_time",)
