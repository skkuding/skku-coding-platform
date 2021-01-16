from django.db import models
from django.utils import timezone


class JudgeServer(models.Model):
    hostname = models.TextField()
    ip = models.TextField(null=True)
    judger_version = models.TextField()
    cpu_core = models.IntegerField()
    memory_usage = models.FloatField()
    cpu_usage = models.FloatField()
    last_heartbeat = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    task_number = models.IntegerField(default=0)
    service_url = models.TextField(null=True)
    is_disabled = models.BooleanField(default=False)

    @property
    def status(self):
        # Increase the one-second delay to improve adaptability to the network environment
        if (timezone.now() - self.last_heartbeat).total_seconds() > 6:
            return "abnormal"
        return "normal"

    class Meta:
        db_table = "judge_server"
