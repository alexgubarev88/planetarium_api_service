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
        constraints = [
            UniqueConstraint(fields=["seat", "show_session"], name="unique_ticket_seat_show_session")
        ]

    def __str__(self):
        return f"{self.show_session}, row: {self.row}, seat: {self.seat}"

    def clean(self):
        if not (1 <= self.seat <= self.show_session.planetarium_dome.seats_in_row):
            raise ValueError({
                "seat": f"seat must be in range [1, {self.show_session.planetarium_dome.seats_in_row}], not {self.seat}"
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
