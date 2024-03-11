from django.contrib.auth.models import User

from django.db import models

from todo.models.category_models import Category


class Task(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField(
        max_length=1500,
        verbose_name="task details",
        default="Here you can add your description..."
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
