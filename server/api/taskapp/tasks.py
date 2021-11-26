"""Celery tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.module_loading import import_string
from django.core import management

# Models
from api.sideways.models import Travel

# Celery
from celery.decorators import task

# Utilities
from django.utils import timezone
from datetime import timedelta


@task(name='check_if_trip_has_not_been_activated', max_retries=3)
def check_if_trip_has_not_been_activated():
    """Disable travels has not been activated in 1 minute"""
    now = timezone.now()
    travels = Travel.objects.filter(
        is_active=False,
        is_over=False
    )
    for travel in travels:
        if now > travel.created + timedelta(minutes=20):
            travel.is_over = True
            travel.save()

            # Update stats
            sideway = travel.sideway
            sideway.trips_cancelled += 1
            sideway.save()


# Active to create backups recurrently

# @task(name='do_backup', max_retries=3)
# def do_backup():
#     management.call_command('dbbackup', '-z')
#     print('Backup completed')
