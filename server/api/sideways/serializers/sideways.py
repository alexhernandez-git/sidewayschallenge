"""Sideway serializer."""

# Django

# Django REST Framework
from rest_framework import serializers

# Models
from api.sideways.models import Sideway, Travel, Place

# Serializers


class SidewayModelSerializer(serializers.ModelSerializer):
    """Sideway model serializer."""
    destination = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Meta class."""

        model = Sideway
        fields = (
            'id',
            'place',
            'has_arrived',
            'state',
            'destination'
        )

        read_only_fields = (
            'id',
        )

    def get_destination(self, obj):
        # Get the current travel
        current_travel = Travel.objects.filter(sideway=obj, is_over=False).first()
        # Return the destination
        if current_travel:
            return current_travel.destination.name
        return None


# Request if the trip is possible serializer


class RequestIfTheTripIsPossibleSerializer(serializers.Serializer):
    destination = serializers.CharField()

    def validate(self, data):
        import random

        sideway = self.context['sideway']
        # Validate if you already are on a trip
        if Travel.objects.filter(sideway=sideway, is_over=False).exists():
            raise serializers.ValidationError("You are already on a trip")

        if random.random() < 0.33:
            raise serializers.ValidationError("Trip not possible")
        return data

    def validate_destination(self, data):
        destination_name = data.get('destination')
        destination = Place.objects.filter(destination__name=destination_name).first()
        if not destination:
            raise serializers.ValidationError("This destination not exists")
        return destination

    def create(self, validated_data):
        sideway = self.context['sideway']

        destination = Place.objects.get(name=validated_data['destination'])
        origin = sideway.place
        # If is in here means that the trip is possible so is time to create the trip inactive
        travel = Travel.objects.create(
            sideway=sideway,
            destination=destination,
            origin=origin
        )

        # Update stats
        sideway.trips_accepted += 1
        sideway.save()
        return travel


# Start the trip serializer
class StartTripSerializer(serializers.Serializer):

    def validate(self):
        sideway = self.instance
        travel = Travel.objects.filter(sideway=sideway, is_over=False, is_active=False).first()
        if not travel:
            raise serializers.ValidationError("No travel available")
        return {"travel": travel}

    def update(self, instance, validated_data):
        sideway = instance

        travel = validated_data['travel']
        travel.is_active = True
        travel.is_cancelled = False
        travel.is_over = False
        travel.save()

        # Update stats
        sideway.trips_started += 1
        sideway.save()
        return sideway


# End the trip serializer
class EndTripSerializer(serializers.Serializer):
    def validate(self):
        sideway = self.instance
        travel = Travel.objects.filter(sideway=sideway, is_over=False, is_active=True).first()
        if not travel:
            raise serializers.ValidationError("No travel active")
        return {"travel": travel}

    def update(self, instance, validated_data):
        sideway = instance

        travel = validated_data['travel']
        travel.is_over = True
        travel.save()

        # Update stats
        sideway.trips_made += 1
        sideway.save()
        return sideway

# Cancel the trip serializer


class CancelTripSerializer(serializers.Serializer):
    def validate(self):
        sideway = self.instance
        travel = Travel.objects.filter(sideway=sideway, is_over=False).first()
        if not travel:
            raise serializers.ValidationError("No travel active")
        return {"travel": travel}

    def update(self, instance, validated_data):
        sideway = instance
        travel = validated_data['travel']
        sideway.travels_cancelled
        travel.is_cancelled = True
        travel.is_over = True
        travel.save()

        # Update stats
        sideway.trips_cancelled += 1
        sideway.save()
        return travel
