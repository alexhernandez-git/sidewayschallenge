"""Developer model"""

# Django
from django.contrib.gis.db import models

# Utilities
from api.utils.models import BaseModel


class Place(BaseModel):
    name = models.CharField(max_length=256)
    is_default = models.BooleanField(default=False)
