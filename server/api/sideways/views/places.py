"""Users views."""

# Django

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions

# Models
from api.sideways.models import Place

# Serializers
from api.sideways.serializers import (
    PlaceModelSerializer,
    RequestIfTheTripIsPossibleSerializer,
    StartTripSerializer,
    EndTripSerializer,
    CancelTripSerializer
)

# Filters

# Mixins


class PlaceViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Places view set.
    """

    queryset = Place.objects.all()
    lookup_field = "id"
    serializer_class = PlaceModelSerializer
    permissions = []
    pagination_class = None
