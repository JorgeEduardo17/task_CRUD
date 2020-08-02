from django.contrib.auth import get_user_model
from django.db import models


class TaskUser(models.Model):

    name = models.CharField(
        max_length=100,

    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
    )

    description = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    date = models.DateTimeField(
        auto_now=True
    )

    accept = models.BooleanField(
        default=False
    )

    reason = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return 'Task {}'.format(self.name)

    class Meta:
        ordering = ["id"]
        verbose_name = "task"
        verbose_name_plural = "tasks"

