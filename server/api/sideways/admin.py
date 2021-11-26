

from django.contrib import admin

# Models
from api.sideways.models import (Place,
                                 Sideway,
                                 Travel)

# Register your models here.


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "is_default")


@admin.register(Sideway)
class SidewayAdmin(admin.ModelAdmin):

    list_display = ("id", "place", "has_arrived", "state")


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):

    list_display = ("id", "origin", "destination", "sideway", "is_active", "is_over", "is_cancelled")
