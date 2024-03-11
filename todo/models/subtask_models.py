from django.contrib.auth.models import User
from django.db import models

from todo.models.task_models import Task


class SubTask(models.Model):
    title = models.CharField(max_length=75, blank=True)
    description = models.CharField(max_length=1500, blank=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
        blank=True,
        null=True
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title[:10]}..."

    class Meta:
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
