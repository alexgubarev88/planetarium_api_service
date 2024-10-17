from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet
)

app_name = "planetarium"


router = routers.DefaultRouter()
router.register("show_themes", ShowThemeViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)

urlpatterns = [
    path("", include(router.urls))
]
