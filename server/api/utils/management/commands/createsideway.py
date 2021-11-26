from django.core.management.base import BaseCommand
from api.sideways.models import Sideway, Place


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create places
        Place.objects.create(name="Farmacia")
        Place.objects.create(name="Oncologia")
        Place.objects.create(name="Radiologia")
        Sideway.objects.create(
            id="PHX-001",
            place=Place.objects.create(name="Estación de carga", is_default=True)
        )
