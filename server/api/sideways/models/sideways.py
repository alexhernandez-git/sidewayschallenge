"""Organization model"""

# Django
from django.db.models.fields.related import ManyToManyField
from django.contrib.gis.db import models

# Utilities
from api.utils.models import BaseModel


class Sideway(BaseModel):
    id = models.CharField(primary_key=True, max_length=256)

    place = models.ForeignKey("sideways.Place", on_delete=models.SET_NULL, null=True)

    has_arrived = models.BooleanField(default=False)

    FREE = "FR"
    BUSY = "BU"
    TYPE_CHOICES = [
        (FREE, 'Free'),
        (BUSY, 'Busy'),
    ]
    state = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=FREE
    )
    trips_completed = models.IntegerField(default=0, help_text='Trips completed succesfully.')
    trips_started = models.IntegerField(default=0)
    trips_cancelled = models.IntegerField(default=0)
    trips_timeout = models.IntegerField(default=0, help_text='Trips accepted but not action maked.')
    trips_accepted = models.IntegerField(default=0, help_text='Trips that has been accepted.')
