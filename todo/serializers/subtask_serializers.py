from django.contrib.auth.models import User
from rest_framework import serializers

from todo.error_messages import (
    TITLE_REQUIRED_ERROR,
    TITLE_SUBTASK_LENGTH_ERROR,
    DESCRIPTION_SUBTASK_LENGTH_ERROR,
)
from todo.models.subtask_models import SubTask
from todo.models.task_models import Task


def validate_fields(attrs):
    title = attrs.get('title')
    description = attrs.get('description')

    if title is None:
        raise serializers.ValidationError(
            TITLE_REQUIRED_ERROR
        )
    if title and len(title) > 75:
        raise serializers.ValidationError(
            TITLE_SUBTASK_LENGTH_ERROR
        )
    if description and len(description) > 1499:
        raise serializers.ValidationError(
            DESCRIPTION_SUBTASK_LENGTH_ERROR
        )

    return attrs


class ListSubTasksSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    task = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Task.objects.all()
    )

    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'description',
            'task',
            'creator',
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)


class SubTaskInfoSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    task = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Task.objects.all()
    )

    class Meta:
        model = SubTask
        fields = [
            'id',
            'title',
            'description',
            'task',
            'creator',
            'created_at',
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)
