from django.db import models
from django.db.models import UniqueConstraint

from planetarium_api_service import settings


class AstronomyShow(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()
    show_theme = models.ManyToManyField("ShowTheme", related_name="show_themes")

    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Theme: {self.show_theme}"


class ShowTheme(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def size(self):
        return "large" if self.rows >= 5 else "medium"

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f" {self.name} ({self.rows} rows, {self.seats_in_row} seats in row)"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show} at {self.planetarium_dome} on {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} at {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ["seat", "show_session"]

    def __str__(self):
        return f"{self.show_session}, row: {self.row}, seat: {self.seat}"

    @staticmethod
    def validate_seat(seat: int, num_seats: int, error_to_raise):
        if not (1 <= seat <= num_seats):
            raise error_to_raise({
                "seat": f"seat must be in range [1, {Ticket.show_session.planetarium_dome.seats_in_row}], not {seat}"
            })

    def clean(self):
        Ticket.validate_seat(self.seat, Ticket.show_session.planetarium_dome.capacity, ValueError)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
