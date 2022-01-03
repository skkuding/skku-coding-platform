from django.db import models


class Banner(models.Model):
    title = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    visible = models.BooleanField(default=False)

    class Meta:
        db_table = "banner"
        ordering = ("-create_time",)
