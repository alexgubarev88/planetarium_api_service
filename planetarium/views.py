from rest_framework import viewsets

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
    PlanetariumDomeSerializer,
    ShowSessionListSerializer
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        else:
            return ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related()
        else:
            return queryset


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
