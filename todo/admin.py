from django.contrib import admin

from todo.models.category_models import Category
from todo.models.task_models import Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'created_at')
    list_filter = ('category', 'creator', 'created_at')
    search_fields = ('title',)
