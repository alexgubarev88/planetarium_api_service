from django.db import models

from planetarium_api_service import settings


class AstronomyShow(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()
    show_theme = models.ForeignKey("ShowTheme", on_delete=models.DO_NOTHING)

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

    def __str__(self):
        return f"{self.user} at {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f"{self.show_session}, row: {self.row}, seat: {self.seat}"
