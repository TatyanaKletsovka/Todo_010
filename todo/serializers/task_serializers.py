from rest_framework import serializers

from todo.error_messages import (
    TITLE_REQUIRED_ERROR,
    TITLE_LENGTH_ERROR,
    DESCRIPTION_LENGTH_ERROR,
)
from todo.models.task_models import Task


def validate_fields(attrs):
    title = attrs.get('title')
    description = attrs.get('description')

    if not title:
        raise serializers.ValidationError(
            TITLE_REQUIRED_ERROR
        )
    if len(title) > 75:
        raise serializers.ValidationError(
            TITLE_LENGTH_ERROR
        )
    if description and len(description) > 1499:
        raise serializers.ValidationError(
            DESCRIPTION_LENGTH_ERROR
        )
    return attrs


class TaskInfoSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'category',
            'created_at',
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)


class AllTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'creator',
            'category',
            'created_at'
        ]

    def validate(self, attrs):
        return validate_fields(attrs=attrs)
