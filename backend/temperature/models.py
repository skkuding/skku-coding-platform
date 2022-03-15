from django.db import models


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
    user_id = models.IntegerField(unique=True)
    temperature = models.IntegerField(default=0)

    class Meta:
        db_table = "temperature"
        ordering = ("-temperature",)


class SolvedProblem(models.Model):
    user_id = models.IntegerField(db_index=True)
    id = models.TextField(primary_key=True, db_index=True)
    score = models.IntegerField()
    solved_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "solvedproblem"
