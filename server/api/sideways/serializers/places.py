"""Place serializer."""

# Django

# Django REST Framework
from rest_framework import serializers

# Models
from api.sideways.models import Place

# Serializers


class PlaceModelSerializer(serializers.ModelSerializer):
    """Place model serializer."""

    class Meta:
        """Meta class."""

        model = Place
        fields = (
            'id',
            'name',
            'is_default',
        )

        read_only_fields = (
            'id',
        )
