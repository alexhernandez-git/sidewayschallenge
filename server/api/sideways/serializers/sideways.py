"""Sideway serializer."""

# Django

# Django REST Framework
from rest_framework import serializers

# Models
from api.sideways.models import Sideway, Travel, Place

# Serializers


class SidewayModelSerializer(serializers.ModelSerializer):
    """Sideway model serializer."""
    place_name = serializers.SerializerMethodField(read_only=True)
    destination = serializers.SerializerMethodField(read_only=True)
    pending_to_accept = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Meta class."""

        model = Sideway
        fields = (
            'id',
            'place_name',
            'has_arrived',
            'state',
            'destination',
            'pending_to_accept'
        )

        read_only_fields = (
            'id',
        )

    def get_place_name(self, obj):
        if obj.place:
            return obj.place.name

    def get_destination(self, obj):
        # Get the current travel
        current_travel = Travel.objects.filter(sideway=obj, is_over=False).first()
        # Return the destination
        if current_travel:
            return current_travel.destination.name
        return None

    def get_pending_to_accept(self, obj):
        # Get the current travel
        current_travel = Travel.objects.filter(sideway=obj, is_over=False, is_active=False).first()
        # Return the destination
        if current_travel:
            return True
        return False

# Request if the trip is possible serializer


class RequestIfTheTripIsPossibleSerializer(serializers.Serializer):
    destination = serializers.CharField()

    def validate(self, data):
        import random

        sideway = self.context['sideway']
        # Validate if you already are on a inactive trip
        if Travel.objects.filter(sideway=sideway, is_over=False, is_active=False).exists():
            raise serializers.ValidationError("You must accept or cancel your pending trip")
        # Validate if you already are on a trip
        if Travel.objects.filter(sideway=sideway, is_over=False, is_active=True).exists():
            raise serializers.ValidationError("You are already on a trip")
        if random.random() < 0.33:
            raise serializers.ValidationError("Trip not possible")
        return data

    def validate_destination(self, data):
        destination_name = data
        sideway = self.context['sideway']
        destination = Place.objects.filter(name=destination_name).first()
        if not destination:
            raise serializers.ValidationError("This destination not exists")
        if destination.is_default:
            raise serializers.ValidationError("User cannot choice the default destination")
        if sideway.place == destination:
            raise serializers.ValidationError("Destination selected can't be your current location")
        return destination

    def create(self, validated_data):
        sideway = self.context['sideway']

        destination = validated_data['destination']

        origin = sideway.place

        # If is in here means that the trip is possible so is time to create the trip inactive
        Travel.objects.create(
            sideway=sideway,
            destination=destination,
            origin=origin
        )

        # Update stats
        sideway.trips_accepted += 1
        sideway.save()
        return sideway


# Start the trip serializer
class StartTripSerializer(serializers.Serializer):

    def validate(self, data):
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

        # Update sideway place
        sideway.place = travel.destination
        sideway.has_arrived = False

        # Update stats
        sideway.trips_started += 1
        sideway.save()
        return sideway


# End the trip serializer
class EndTripSerializer(serializers.Serializer):
    def validate(self, data):
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

        # Update sideway place
        sideway.has_arrived = True

        # Update stats
        sideway.trips_completed += 1
        sideway.save()
        return sideway

# Cancel the trip serializer


class CancelTripSerializer(serializers.Serializer):
    def validate(self, data):
        sideway = self.instance
        travel = Travel.objects.filter(sideway=sideway, is_over=False).first()
        if not travel:
            raise serializers.ValidationError("No travel active")
        return {"travel": travel}

    def update(self, instance, validated_data):
        sideway = instance
        travel = validated_data['travel']
        travel.is_cancelled = True
        travel.is_over = True
        travel.save()

        # Update sideway place
        sideway.place = travel.origin
        sideway.has_arrived = True

        # Update stats
        sideway.trips_cancelled += 1
        sideway.save()
        return sideway
