

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import sideways as sideway_views
from .views import places as place_views

router = DefaultRouter()

router.register(r'sideways', sideway_views.SidewayViewSet, basename='sideways')
router.register(r'places', place_views.PlaceViewSet, basename='places')

urlpatterns = [
    path('', include(router.urls))
]
