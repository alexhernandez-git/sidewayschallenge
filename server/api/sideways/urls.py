

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import sideways as sideway_views

router = DefaultRouter()

router.register(r'sideways', sideway_views.SidewayViewSet, basename='sideways')

urlpatterns = [
    path('', include(router.urls))
]
