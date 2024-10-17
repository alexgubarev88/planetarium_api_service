from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from planetarium.models import (
    ShowTheme,
    ShowSession,
    AstronomyShow,
    Reservation,
    PlanetariumDome
)
from planetarium.serializers import (
    ShowThemeSerializer,
    ShowSessionSerializer,
    AstronomyShowSerializer,
    ReservationSerializer,
    PlanetariumDomeSerializer
)


class ShowThemeViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class AstronomyShowViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin
):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer


class ShowSessionViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer


class ReservationViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

