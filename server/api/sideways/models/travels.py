"""Organization model"""

# Django
from django.db.models.fields.related import ManyToManyField
from django.contrib.gis.db import models

# Utilities
from api.utils.models import BaseModel


class Travel(BaseModel):
    origin = models.ForeignKey("sideways.Place", on_delete=models.SET_NULL,
                               null=True, blank=True, related_name="travel_origin")

    destination = models.ForeignKey("sideways.Place", on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name="travel_destination")
    sideway = models.ForeignKey("sideways.Sideway", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_over = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
