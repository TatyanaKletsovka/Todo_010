from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todo.error_messages import NON_UNIQUE_CATEGORY_NAME_ERROR, CATEGORY_NAME_LEN_ERROR
from todo.models.category_models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError(
                NON_UNIQUE_CATEGORY_NAME_ERROR
            )

        if len(value) < 4 or len(value) > 25:
            raise ValidationError(
                CATEGORY_NAME_LEN_ERROR
            )

        return value
