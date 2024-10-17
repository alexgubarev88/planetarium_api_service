from rest_framework import serializers

from planetarium.models import (
    Ticket,
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    Reservation,
    ShowSession
)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Model:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Model:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")
