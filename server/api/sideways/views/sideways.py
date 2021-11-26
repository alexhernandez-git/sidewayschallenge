"""Users views."""

# Django

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions

# Models
from api.sideways.models import Sideway

# Serializers
from api.sideways.serializers import (
    SidewayModelSerializer,
    RequestIfTheTripIsPossibleSerializer,
    StartTripSerializer,
    EndTripSerializer,
    CancelTripSerializer
)

# Filters

# Mixins


class SidewayViewSet(
    viewsets.GenericViewSet,
):
    """Sideways view set.
    """

    queryset = Sideway.objects.all()
    lookup_field = "id"
    serializer_class = SidewayModelSerializer
    permissions = []
    pagination_class = None

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        if self.action in ['requesst_if_the_trip_is_possible']:
            return {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self,
                'sideway': self.get_object()
            }

        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        if self.action in ['request_if_the_trip_is_possible']:
            return RequestIfTheTripIsPossibleSerializer
        elif self.action in ['start_trip']:
            return StartTripSerializer
        elif self.action in ['end_trip']:
            return EndTripSerializer
        elif self.action in ['cancel_trip']:
            return CancelTripSerializer
        return self.serializer_class

    # Retrieve available sideway ['get']
    @action(detail=False, methods=['get'])
    def retrieve_available_sideway(self, request, *args, **kwargs):
        sideway = Sideway.objects.filter(state=Sideway.FREE).first()
        if not sideway:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(SidewayModelSerializer(sideway).data)

    # Request if the trip is possible ['post']
    @action(detail=True, methods=['post'])
    def request_if_the_trip_is_possible(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    # Start the trip ['patch']
    @action(detail=True, methods=['patch'])
    def start_trip(self, request, *args, **kwargs):
        sideway = self.get_object()

        partial = request.method == 'PATCH'
        serializer = self.get_serializer(
            sideway,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        sideway = serializer.save()
        data = SidewayModelSerializer(sideway).data
        return Response(data, status=status.HTTP_200_OK)

    # End the trip ['patch']
    @action(detail=True, methods=['patch'])
    def end_trip(self, request, *args, **kwargs):
        sideway = self.get_object()

        partial = request.method == 'PATCH'
        serializer = self.get_serializer(
            sideway,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        sideway = serializer.save()
        data = SidewayModelSerializer(sideway).data
        return Response(data, status=status.HTTP_200_OK)

    # Cancel the trip ['patch']
    @action(detail=True, methods=['patch'])
    def cancel_trip(self, request, *args, **kwargs):
        sideway = self.get_object()

        partial = request.method == 'PATCH'
        serializer = self.get_serializer(
            sideway,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        sideway = serializer.save()
        data = SidewayModelSerializer(sideway).data
        return Response(data, status=status.HTTP_200_OK)
